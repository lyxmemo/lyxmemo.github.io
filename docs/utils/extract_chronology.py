#!/usr/bin/env python3
"""
One-time extraction script: parse chronology.html into structured YAML.
Uses only Python stdlib (no BeautifulSoup).
"""
import re
import html
import os


# ── Paths ──────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.dirname(SCRIPT_DIR)
HTML_PATH = os.path.join(DOCS_DIR, "chronology.html")
YAML_PATH = os.path.join(DOCS_DIR, "_data", "chronology.yml")


# ── Helpers ────────────────────────────────────────────────────────────────
def strip_tags(s):
    """Remove all HTML tags, decode entities."""
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(s).strip()


def yaml_str(s):
    """Escape a string for YAML double-quoted output."""
    if not s:
        return '""'
    s = s.replace('\\', '\\\\').replace('"', '\\"')
    return f'"{s}"'


def indent_block(s, n=8):
    """For multi-line YAML strings, use literal block scalar."""
    lines = s.strip().split('\n')
    if len(lines) == 1:
        return yaml_str(lines[0])
    prefix = ' ' * n
    return '|\n' + '\n'.join(prefix + l for l in lines)


def find_matching_close_tag(html_str, tag, start_pos):
    """
    Given html_str starting after an opening <tag ...>, find the position
    of the matching </tag>. Handles nested tags of the same type.
    Returns the index of the start of </tag>.
    """
    depth = 1
    pos = start_pos
    open_pat = re.compile(rf'<{tag}[\s>]', re.I)
    close_pat = re.compile(rf'</{tag}>', re.I)
    while depth > 0 and pos < len(html_str):
        next_open = open_pat.search(html_str, pos)
        next_close = close_pat.search(html_str, pos)
        if next_close is None:
            return len(html_str)
        if next_open and next_open.start() < next_close.start():
            depth += 1
            pos = next_open.end()
        else:
            depth -= 1
            if depth == 0:
                return next_close.start()
            pos = next_close.end()
    return len(html_str)


def split_entries(entries_html):
    """Split entries_html into individual entry blocks, handling nested divs."""
    results = []
    pat = re.compile(r'<div class="chronology-entry">')
    for m in pat.finditer(entries_html):
        start_content = m.end()
        # Find matching closing </div> for this entry
        close_pos = find_matching_close_tag(entries_html, 'div', start_content)
        entry_inner = entries_html[start_content:close_pos]
        results.append(entry_inner)
    return results


def normalize_date(year, raw_date):
    """
    Return (iso_date, date_display) based on raw date text.
    """
    d = raw_date.strip()
    if not d:
        return ("", "")

    non_standard = ["春", "夏", "秋", "冬", "同年", "年末", "春节后", "元月上旬"]
    if d in non_standard:
        return ("", d)

    # "8月21-23日" style
    m = re.match(r'^(\d{1,2})月(\d{1,2})-(\d{1,2})日$', d)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        return (f"{year}-{month:02d}-{day:02d}", d)

    # "12月25日"
    m = re.match(r'^(\d{1,2})月(\d{1,2})日$', d)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        return (f"{year}-{month:02d}-{day:02d}", "")

    # "5月"
    m = re.match(r'^(\d{1,2})月$', d)
    if m:
        return (f"{year}-{int(m.group(1)):02d}", "")

    # "9/2"
    m = re.match(r'^(\d{1,2})/(\d{1,2})$', d)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        return (f"{year}-{month:02d}-{day:02d}", "")

    return ("", d)


def extract_source_from_content(content_text):
    """
    Try to extract source citations embedded in content text.
    Returns (cleaned_content, source_text, source_url).
    """
    source = ""
    source_url = ""
    text = content_text

    # Pattern: （中缅印战区盟军将帅图志Pnnn）
    m = re.search(r'[（(](中缅印战区盟军将帅图志[^）)]*)[）)]', text)
    if m:
        source = m.group(1)
        text = text[:m.start()] + text[m.end():]
        text = text.strip()

    # Pattern: Stillwell's Command Problems Pnnn
    m = re.search(r"(Stillwell's Command Problems\s+P\d+)", text)
    if m:
        if source:
            source += "; " + m.group(1)
        else:
            source = m.group(1)
        text = text[:m.start()] + text[m.end():]
        text = text.strip()

    return text.strip(), source, source_url


def parse_source_div(div_html):
    """Parse <div class="chronology-source">...</div>."""
    text = strip_tags(div_html)
    urls = re.findall(r'href="([^"]*)"', div_html)
    source_url = urls[0] if urls else ""
    text = re.sub(r'^来源[：:]?\s*', '', text).strip()
    if source_url and source_url in text:
        text = text.replace(source_url, '').strip()
    return text, source_url


def parse_details_block(details_html):
    """Parse <details class="chronology-detail-toggle">...</details> → original_text."""
    m = re.search(r'<div class="chronology-detail-text">(.*?)</div>\s*</details>', details_html, re.S)
    if m:
        inner = m.group(1)
        paragraphs = re.findall(r'<p>(.*?)</p>', inner, re.S)
        if paragraphs:
            return '\n'.join(strip_tags(p) for p in paragraphs).strip()
        return strip_tags(inner)
    return ""


def parse_entry(entry_inner, year):
    """
    Parse one entry's inner HTML (after outer <div class="chronology-entry">).
    The entry_inner contains: <div class="chronology-date">...</div>
                              <div class="chronology-content">...</div>
    """
    # Extract date div
    date_match = re.search(r'<div class="chronology-date">(.*?)</div>', entry_inner, re.S)
    raw_date = strip_tags(date_match.group(1)) if date_match else ""

    # Extract content div (everything after date div until the end)
    content_start_match = re.search(r'<div class="chronology-content">', entry_inner)
    if not content_start_match:
        return None
    content_body_start = content_start_match.end()
    content_close = find_matching_close_tag(entry_inner, 'div', content_body_start)
    content_html = entry_inner[content_body_start:content_close].strip()

    iso_date, date_display = normalize_date(year, raw_date)
    is_note_entry = 'class="chronology-note"' in content_html

    # Extract <details> block
    original_text = ""
    details_match = re.search(
        r'<details class="chronology-detail-toggle">.*?</details>',
        content_html, re.S
    )
    if details_match:
        original_text = parse_details_block(details_match.group(0))
        content_html_clean = content_html[:details_match.start()] + content_html[details_match.end():]
    else:
        content_html_clean = content_html

    # Extract <div class="chronology-source">
    source_text = ""
    source_url = ""
    source_match = re.search(
        r'<div class="chronology-source">(.*?)</div>',
        content_html_clean, re.S
    )
    if source_match:
        source_text, source_url = parse_source_div(source_match.group(0))
        content_html_clean = (
            content_html_clean[:source_match.start()]
            + content_html_clean[source_match.end():]
        )

    # Extract <p> content
    p_tags = re.findall(r'<p[^>]*>(.*?)</p>', content_html_clean, re.S)
    notes = ""

    if is_note_entry:
        content = ""
        notes = '\n'.join(strip_tags(p) for p in p_tags)
    else:
        content = '\n'.join(strip_tags(p) for p in p_tags)

        # Extract inline sources
        content, extracted_source, extracted_url = extract_source_from_content(content)
        if extracted_source:
            source_text = (source_text + "; " + extracted_source).lstrip("; ") if source_text else extracted_source
        if extracted_url and not source_url:
            source_url = extracted_url

    # Handle inline dates in content when date fields are empty
    if not iso_date and not date_display and content:
        inline_patterns = [
            (r'^(\d{1,2}[、]\d{1,2}月间)[，,]\s*', lambda m: ("", m.group(1).replace("、", "-"))),
            (r'^(\d{1,2}月初)[，,]\s*', lambda m: ("", m.group(1))),
            (r'^(\d{1,2}月中旬)[，,]\s*', lambda m: ("", m.group(1))),
            (r'^(\d{1,2}月底)[，,]\s*', lambda m: ("", m.group(1))),
        ]
        for pat, handler in inline_patterns:
            im = re.match(pat, content)
            if im:
                iso_date, date_display = handler(im)
                content = content[im.end():].strip()
                break

    # Extract URLs from content for source_url
    if not source_url:
        url_matches = re.findall(r'(https?://[^\s<>）)]+)', content)
        if url_matches:
            source_url = url_matches[0]

    return {
        'date': iso_date,
        'date_display': date_display,
        'content': content,
        'source': source_text,
        'source_url': source_url,
        'original_text': original_text,
        'notes': notes,
    }


# ── Main extraction ────────────────────────────────────────────────────────
def extract_all(html_content):
    """Parse the full HTML and return list of year dicts."""
    years = []

    # Find year sections: <details class="chronology-year-section" id="year-NNNN">
    year_open_pat = re.compile(
        r'<details class="chronology-year-section" id="year-(\d+)">'
    )

    for m in year_open_pat.finditer(html_content):
        year = int(m.group(1))
        section_start = m.end()
        # Find the matching </details>
        section_close = find_matching_close_tag(html_content, 'details', section_start)
        section_html = html_content[section_start:section_close]

        # Find the entries container
        entries_start_match = re.search(r'<div class="chronology-entries">', section_html)
        if not entries_start_match:
            years.append({'year': year, 'entries': []})
            continue

        entries_body_start = entries_start_match.end()
        entries_close = find_matching_close_tag(section_html, 'div', entries_body_start)
        entries_html = section_html[entries_body_start:entries_close]

        # Split into individual entry blocks
        entry_blocks = split_entries(entries_html)
        entries = []
        for block in entry_blocks:
            entry = parse_entry(block, year)
            if entry:
                entries.append(entry)

        years.append({'year': year, 'entries': entries})

    return years


def write_yaml(years, path):
    """Write structured YAML output manually (to avoid pyyaml dependency)."""
    lines = []
    for ydata in years:
        lines.append(f"- year: {ydata['year']}")
        lines.append("  entries:")
        for e in ydata['entries']:
            lines.append(f"    - date: {yaml_str(e['date'])}")
            lines.append(f"      date_display: {yaml_str(e['date_display'])}")
            lines.append(f"      content: {indent_block(e['content'])}")
            lines.append(f"      source: {yaml_str(e['source'])}")
            lines.append(f"      source_url: {yaml_str(e['source_url'])}")
            if e['original_text']:
                lines.append(f"      original_text: {indent_block(e['original_text'])}")
            else:
                lines.append(f"      original_text: \"\"")
            if e['notes']:
                lines.append(f"      notes: {indent_block(e['notes'])}")
            else:
                lines.append(f"      notes: \"\"")

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    print(f"Wrote {len(years)} years to {path}")
    total = sum(len(y['entries']) for y in years)
    print(f"Total entries: {total}")


if __name__ == '__main__':
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    years = extract_all(content)
    write_yaml(years, YAML_PATH)
