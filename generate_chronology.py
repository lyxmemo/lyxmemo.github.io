#!/usr/bin/env python3
"""Parse np.txt and npsy.txt and generate chronology.html for the Jekyll site."""

import re
import html


def parse_np(filepath):
    """Parse the main chronology file (np.txt).
    Returns dict: year (str) -> list of entry strings.
    """
    years = {}
    current_year = None
    current_entries = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.rstrip('\n')
        if line.strip() == '年谱' and not current_year:
            continue
        m = re.match(r'^【(\d{4})】$', line.strip())
        if m:
            if current_year is not None:
                years[current_year] = current_entries
            current_year = m.group(1)
            current_entries = []
            continue
        if line.strip() and current_year is not None:
            current_entries.append(line.strip())

    if current_year is not None:
        years[current_year] = current_entries
    return years


# Patterns that indicate a new entry headline (NOT detail text)
ENTRY_DATE_PATTERNS = [
    r'^\d{1,2}月\d{1,2}日',           # 5月16日
    r'^\d{1,2}月\s',                   # 5月 (month only, followed by space)
    r'^元月',                           # 元月
    r'^\d{1,2}/\d{1,2}',              # 7/15
    r'^国庆观礼',
]

def is_entry_headline(line):
    """Check if line starts a new entry (date-prefixed headline).

    Lines like "1月19日新22师66团..." -> True (new entry)
    Lines like "1943年11月30日，蒋介石夫妇..." -> False (detail text, has year prefix)
    Lines like "《申报》1946年01月03日..." -> False (citation)
    """
    if not line or not line.strip():
        return False
    line = line.strip()

    # Exclude lines that start with YYYY年 (those are citation dates or detail text)
    if re.match(r'^\d{4}年', line):
        return False

    for pat in ENTRY_DATE_PATTERNS:
        if re.match(pat, line):
            return True
    return False


def is_source_line(line):
    """Check if a line is a source reference."""
    s = line.strip().lower()
    return s.startswith('source:') or s.startswith('[source:')


def is_page_ref(line):
    """Check if a line is a page reference like P123."""
    return bool(re.match(r'^P\d+', line.strip()))


def parse_npsy(filepath):
    """Parse the supplementary chronology file (npsy.txt)."""
    years = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    year_pattern = re.compile(r'^(\d{4})年?\s*$', re.MULTILINE)
    year_matches = list(year_pattern.finditer(content))

    for idx, match in enumerate(year_matches):
        year = match.group(1)
        start = match.end()
        end = year_matches[idx + 1].start() if idx + 1 < len(year_matches) else len(content)
        section = content[start:end].strip()
        if not section:
            continue
        entries = parse_npsy_section(section)
        if entries:
            years[year] = entries
    return years


def parse_npsy_section(section_text):
    """Parse a year section from npsy.txt using line-by-line state machine.

    Entry detection: a line matching ENTRY_DATE_PATTERNS starts a new entry.
    Source lines (source: ...) and page refs (P123) are attached to the current entry.
    Everything else is detail text for the current entry.
    """
    lines = section_text.split('\n')
    entries = []
    current = None  # Current entry being built

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip header
        if stripped == '年谱拾遗':
            i += 1
            continue

        # Skip blank lines (but note them for context)
        if not stripped:
            i += 1
            continue

        # Check if this line starts a new entry
        if is_entry_headline(stripped):
            # Save previous entry
            if current:
                entries.append(finalize_entry_lines(current))
            current = {
                'headline': stripped,
                'source_blocks': [],
                'detail_lines': [],
                '_in_source': False,
                '_current_source_lines': [],
            }
            i += 1
            continue

        # If no current entry, start one anyway (handles non-date-prefixed entries)
        if current is None:
            current = {
                'headline': stripped,
                'source_blocks': [],
                'detail_lines': [],
                '_in_source': False,
                '_current_source_lines': [],
            }
            i += 1
            continue

        # Source line
        if is_source_line(stripped):
            # Flush any pending source
            if current['_current_source_lines']:
                current['source_blocks'].append('\n'.join(current['_current_source_lines']))
            current['_current_source_lines'] = [stripped]
            current['_in_source'] = True
            i += 1
            continue

        # Page reference (P123) - part of source if we're in a source block
        if is_page_ref(stripped) and current['_in_source']:
            current['_current_source_lines'].append(stripped)
            i += 1
            continue

        # URL line continuation of source
        if stripped.startswith('http') and current['_in_source']:
            current['_current_source_lines'].append(stripped)
            i += 1
            continue

        # Source metadata continuation (document titles, reference numbers)
        if current['_in_source'] and is_source_metadata(stripped):
            current['_current_source_lines'].append(stripped)
            i += 1
            continue

        # End source block, this is detail text
        if current['_in_source']:
            current['source_blocks'].append('\n'.join(current['_current_source_lines']))
            current['_current_source_lines'] = []
            current['_in_source'] = False

        # Detail text
        current['detail_lines'].append(stripped)
        i += 1

    # Save last entry
    if current:
        entries.append(finalize_entry_lines(current))

    return entries


def is_source_metadata(line):
    """Check if a line is metadata continuation of a source block."""
    prefixes = [
        'FOREIGN RELATIONS',
        '893.',
        'Marshall Mission',
        'Representative ',
        'Minutes of ',
        'Mukden,',
        'Washington,',
        'The Consul',
        '[Received',
        '[Page',
    ]
    for p in prefixes:
        if line.startswith(p):
            return True
    return False


def finalize_entry_lines(raw):
    """Convert raw entry data into final form."""
    # Flush any pending source
    if raw['_current_source_lines']:
        raw['source_blocks'].append('\n'.join(raw['_current_source_lines']))

    return {
        'headline': raw['headline'],
        'detail': '\n'.join(raw['detail_lines']).strip(),
        'sources': raw['source_blocks'],
    }


def escape(text):
    return html.escape(text)


def format_entry_text(text):
    """Format entry text, converting URLs to links."""
    escaped = escape(text)
    url_pattern = r'(https?://[^\s\]）》」&;]+)'
    escaped = re.sub(url_pattern, r'<a href="\1" target="_blank" rel="noopener">\1</a>', escaped)
    return escaped


def format_source(source_text):
    """Format a source citation block."""
    lines = source_text.split('\n')
    formatted_parts = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith('source:'):
            line = line[7:].strip()
        if line.lower().startswith('[source:'):
            line = line[8:].strip()
            line = line.rstrip('];').strip()
        escaped = escape(line)
        url_pattern = r'(https?://[^\s\]）》」;&]+)'
        escaped = re.sub(url_pattern, r'<a href="\1" target="_blank" rel="noopener">\1</a>', escaped)
        formatted_parts.append(escaped)
    return '<br>'.join(formatted_parts)


def extract_date_and_content(text):
    """Extract date portion and content from an entry line.
    Returns (date_str, content_str, is_note).
    """
    text = text.strip()

    # Annotation/note
    if text.startswith('按：') or text.startswith('注：') or text.startswith('注①') or text.startswith('注②'):
        return ('', text, True)

    # "MM月DD日-DD日" date range
    m = re.match(r'^(\d{1,2}月\d{1,2}日?[-至]\d{1,2}日?)[\s，、]*(.*)', text, re.DOTALL)
    if m:
        return (m.group(1), m.group(2).strip(), False)

    # "MM月DD日"
    m = re.match(r'^(\d{1,2}月\d{1,2}日)[\s，、]*(.*)', text, re.DOTALL)
    if m:
        return (m.group(1), m.group(2).strip(), False)

    # "MM月" (month only, needs separator)
    m = re.match(r'^(\d{1,2}月)[\s，、]+(.*)', text, re.DOTALL)
    if m:
        return (m.group(1), m.group(2).strip(), False)

    # "YYYY年MM月DD日"
    m = re.match(r'^(\d{4}年\d{1,2}月\d{1,2}日)\s*(.*)', text, re.DOTALL)
    if m:
        return (m.group(1), m.group(2).strip(), False)

    # Seasonal/period markers
    m = re.match(r'^(元月[上中下]旬|春节?后?|夏|秋|冬|年末|年底|同年|拂晓)[\s，、]*(.*)', text, re.DOTALL)
    if m:
        return (m.group(1), m.group(2).strip(), False)

    # "M/D"
    m = re.match(r'^(\d{1,2}/\d{1,2})\s*(.*)', text, re.DOTALL)
    if m:
        return (m.group(1), m.group(2).strip(), False)

    return ('', text, False)


def format_detail(text):
    """Format detail/newspaper text for collapsed display."""
    lines = text.split('\n')
    paragraphs = []
    current = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current:
                paragraphs.append(' '.join(current))
                current = []
        elif stripped.startswith('▲') or stripped.startswith('〔'):
            if current:
                paragraphs.append(' '.join(current))
                current = []
            current.append(stripped)
        else:
            current.append(stripped)

    if current:
        paragraphs.append(' '.join(current))

    formatted = []
    for p in paragraphs:
        if p.strip():
            formatted.append(f'<p>{format_entry_text(p)}</p>')
    return '\n'.join(formatted)


def date_sort_key(date_str):
    """Return a (month, day) tuple for sorting entries chronologically."""
    if not date_str:
        return (50, 0)
    s = date_str.strip()
    # 元月
    if s.startswith('元月'):
        d = re.search(r'(\d{1,2})日', s)
        return (1, int(d.group(1)) if d else 0)
    # MM月DD日
    m = re.match(r'^(\d{1,2})月(\d{1,2})日', s)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    # MM月
    m = re.match(r'^(\d{1,2})月', s)
    if m:
        return (int(m.group(1)), 0)
    # M/D
    m = re.match(r'^(\d{1,2})/(\d{1,2})', s)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    # Seasonal
    for keyword, order in [('春', 60), ('夏', 61), ('秋', 62), ('冬', 63),
                           ('年末', 64), ('年底', 64)]:
        if keyword in s:
            return (order, 0)
    return (50, 0)


def generate_html(np_data, npsy_data):
    """Generate the chronology.html content."""
    all_years = sorted(set(list(np_data.keys()) + list(npsy_data.keys())))

    parts = []

    # Build year navigation data grouped by decade
    decade_groups = {}
    for year in all_years:
        decade = (int(year) // 10) * 10
        decade_groups.setdefault(decade, []).append(year)

    # Front matter and styles
    parts.append("""---
layout: default
title: 年谱
---

<style>
.chronology-header {
  margin-bottom: 1.5rem;
}
.chronology-header h1 {
  font-size: 1.8rem;
  margin-bottom: 0.3rem;
}
.chronology-header p {
  color: #666;
  font-size: 0.9rem;
  margin: 0.2rem 0;
}

.chronology-year-nav {
  background: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 0.8rem 1rem;
  margin-bottom: 1.5rem;
}
.chronology-year-nav-row {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  padding: 0.2rem 0;
  flex-wrap: wrap;
}
.chronology-decade-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #999;
  min-width: 45px;
  flex-shrink: 0;
}
.chronology-year-link {
  font-size: 0.85rem;
  color: #2563eb;
  text-decoration: none;
  padding: 2px 6px;
  border-radius: 3px;
  cursor: pointer;
}
.chronology-year-link:hover {
  background-color: #e8f0fe;
  text-decoration: none;
}

.chronology-year-section {
  border-bottom: 1px solid #e0e0e0;
  transition: background-color 1.5s;
}
.chronology-year-section:first-of-type {
  border-top: 1px solid #e0e0e0;
}
.chronology-year-section.highlight {
  background-color: #fffde7;
  transition: background-color 0s;
}
.chronology-year-summary {
  font-size: 1.1rem;
  font-weight: 700;
  padding: 0.6rem 0;
  cursor: pointer;
  list-style: none;
  outline: none;
  margin-bottom: 0 !important;
  transition: background-color 0.2s;
  color: #504949;
}
.chronology-year-summary:hover {
  background-color: #f7f7f7;
}
.chronology-year-summary::-webkit-details-marker { display: none; }
.chronology-year-summary::before {
  content: '\\2212';
  font-family: monospace;
  font-weight: bold;
  font-size: 1rem;
  margin-right: 12px;
  color: #888;
  display: inline-block;
  width: 20px;
  text-align: center;
}
details.chronology-year-section:not([open]) > .chronology-year-summary::before {
  content: '+';
}

.chronology-entries {
  padding: 0 0 1rem 0;
  margin: 0;
}

.chronology-entry {
  display: flex;
  gap: 1rem;
  padding: 0.35rem 0;
  align-items: flex-start;
}
.chronology-date {
  flex-shrink: 0;
  min-width: 85px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #555;
  padding-top: 2px;
}

.chronology-content {
  flex: 1;
  min-width: 0;
}

.chronology-content p {
  margin: 0 0 0.3rem 0;
  line-height: 1.7;
  overflow-wrap: break-word;
  word-break: break-word;
}

.chronology-source {
  font-size: 0.8rem;
  color: #888;
  margin-top: 0.3rem;
  line-height: 1.5;
  word-break: break-all;
}
.chronology-source a {
  color: #6b8eb5;
  text-decoration: none;
}
.chronology-source a:hover {
  text-decoration: underline;
}

.chronology-note {
  font-size: 0.85rem;
  color: #777;
  font-style: italic;
  margin-top: 0.2rem;
  line-height: 1.6;
  overflow-wrap: break-word;
  word-break: break-word;
}

.chronology-detail-toggle {
  margin-top: 0.4rem;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  background-color: #fafafa;
}
.chronology-detail-toggle summary {
  font-size: 0.8rem;
  color: #888;
  cursor: pointer;
  padding: 4px 10px;
  margin-bottom: 0 !important;
  font-weight: normal;
}
.chronology-detail-toggle summary:hover {
  background-color: #f0f0f0;
}
.chronology-detail-toggle summary::before {
  content: '' !important;
  margin-right: 0 !important;
  width: 0 !important;
}
.chronology-detail-text {
  padding: 8px 12px;
  font-size: 0.82rem;
  color: #555;
  line-height: 1.7;
  border-top: 1px solid #e8e8e8;
  max-height: 400px;
  overflow-y: auto;
  overflow-wrap: break-word;
  word-break: break-word;
}
.chronology-detail-text p {
  margin: 0.4rem 0;
}

@media (max-width: 600px) {
  .chronology-entry {
    flex-direction: column;
    gap: 0.2rem;
  }
  .chronology-date {
    min-width: auto;
    font-size: 0.8rem;
    color: #888;
  }
  .chronology-year-nav-row {
    gap: 0.3rem;
  }
  .chronology-decade-label {
    min-width: 40px;
  }
}

.chronology-toggle-wrapper {
  position: fixed;
  bottom: 170px;
  right: 30px;
  z-index: 1000;
}
.chronology-toggle-btn {
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid #ccc;
  color: #333;
  padding: 8px 15px;
  cursor: pointer;
  font-size: 14px;
  border-radius: 20px;
  outline: none;
  box-shadow: 0 2px 10px rgba(0,0,0,0.15);
  transition: all 0.2s ease-in-out;
}
.chronology-toggle-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
</style>

<p><a href="/" style="color:#888;font-size:0.9rem;text-decoration:none;">← 返回主页</a></p>

<div class="chronology-header">
  <h1>年谱</h1>
  <p>依据《抗日名将廖耀湘》等资料整理，报刊杂志及外国档案补充</p>
</div>

<div class="chronology-year-nav">
""")

    # Generate year navigation rows
    for decade in sorted(decade_groups.keys()):
        years_in_decade = decade_groups[decade]
        parts.append(f'  <div class="chronology-year-nav-row">')
        parts.append(f'    <span class="chronology-decade-label">{decade}s</span>')
        for y in years_in_decade:
            parts.append(f'    <a class="chronology-year-link" onclick="jumpToYear(\'year-{y}\')">{y}</a>')
        parts.append(f'  </div>')

    parts.append("""</div>

<div class="chronology-toggle-wrapper">
  <button class="chronology-toggle-btn" onclick="toggleAllChronology()">全部展开/收起</button>
</div>
""")

    for year in all_years:
        np_entries_raw = np_data.get(year, [])
        npsy_entries_raw = npsy_data.get(year, [])

        if not np_entries_raw and not npsy_entries_raw:
            continue

        # Normalize all entries into a unified format for sorting
        unified = []
        for entry_text in np_entries_raw:
            date_str, content_str, is_note = extract_date_and_content(entry_text)
            unified.append({
                'date_str': date_str,
                'content_str': content_str,
                'is_note': is_note,
                'detail': '',
                'sources': [],
            })
        for entry in npsy_entries_raw:
            date_str, content_str, is_note = extract_date_and_content(entry['headline'])
            if not content_str.strip() and not entry['detail'].strip():
                continue
            unified.append({
                'date_str': date_str,
                'content_str': content_str,
                'is_note': is_note,
                'detail': entry['detail'],
                'sources': entry['sources'],
            })

        # Stable sort by date (notes sink to their original position)
        unified.sort(key=lambda e: date_sort_key(e['date_str']))

        parts.append(f'<details class="chronology-year-section" id="year-{year}">')
        parts.append(f'  <summary class="chronology-year-summary">【{year}】</summary>')
        parts.append('  <div class="chronology-entries">')

        for entry in unified:
            if entry['is_note']:
                parts.append('    <div class="chronology-entry">')
                parts.append('      <div class="chronology-date"></div>')
                parts.append('      <div class="chronology-content">')
                parts.append(f'        <p class="chronology-note">{format_entry_text(entry["content_str"])}</p>')
                parts.append('      </div>')
                parts.append('    </div>')
            else:
                parts.append('    <div class="chronology-entry">')
                parts.append(f'      <div class="chronology-date">{escape(entry["date_str"])}</div>')
                parts.append('      <div class="chronology-content">')
                parts.append(f'        <p>{format_entry_text(entry["content_str"])}</p>')

                for source in entry['sources']:
                    formatted_src = format_source(source)
                    if formatted_src.strip():
                        parts.append(f'        <div class="chronology-source">来源：{formatted_src}</div>')

                if entry['detail'].strip():
                    detail_html = format_detail(entry['detail'])
                    parts.append('        <details class="chronology-detail-toggle">')
                    parts.append('          <summary>展开原文</summary>')
                    parts.append(f'          <div class="chronology-detail-text">{detail_html}</div>')
                    parts.append('        </details>')

                parts.append('      </div>')
                parts.append('    </div>')

        parts.append('  </div>')
        parts.append('</details>')
        parts.append('')

    parts.append("""
<script>
function toggleAllChronology() {
  const sections = document.querySelectorAll('.chronology-year-section');
  if (sections.length === 0) return;
  const hasAClosedElement = Array.from(sections).some(s => !s.open);
  sections.forEach(s => { s.open = hasAClosedElement; });
}

function jumpToYear(yearId) {
  const el = document.getElementById(yearId);
  if (!el) return;
  el.open = true;
  el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  el.classList.add('highlight');
  setTimeout(function() { el.classList.remove('highlight'); }, 1500);
}
</script>
""")

    return '\n'.join(parts)


def main():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    np_path = os.path.expanduser('~/np.txt')
    npsy_path = os.path.expanduser('~/npsy.txt')
    output_path = os.path.join(script_dir, 'docs', 'chronology.html')

    print(f"Parsing {np_path}...")
    np_data = parse_np(np_path)
    print(f"  Found {len(np_data)} years in np.txt")

    print(f"Parsing {npsy_path}...")
    npsy_data = parse_npsy(npsy_path)
    print(f"  Found {len(npsy_data)} years in npsy.txt")
    for y in sorted(npsy_data.keys()):
        print(f"    {y}: {len(npsy_data[y])} entries")
        for e in npsy_data[y]:
            h = e['headline'][:70]
            flags = []
            if e['detail']:
                flags.append('detail')
            if e['sources']:
                flags.append(f"{len(e['sources'])} src")
            print(f"      [{h}] {' '.join(flags)}")

    print("\nGenerating chronology.html...")
    html_content = generate_html(np_data, npsy_data)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Written to {output_path}")
    print(f"Total size: {len(html_content)} characters")


if __name__ == '__main__':
    main()
