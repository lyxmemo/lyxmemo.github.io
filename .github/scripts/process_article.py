#!/usr/bin/env python3
"""Parse a GitHub issue body (created from the new-article template),
call the Claude API to format the article content, then write the
markdown file and update changelog.yml."""

import os
import re
import sys
from datetime import date
from pathlib import Path

import anthropic
import yaml

# ── repo paths ──────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[2]  # .github/scripts -> repo root
DOCS = REPO_ROOT / "docs"
CHANGELOG = DOCS / "_data" / "changelog.yml"

# ── fixed category values per collection ────────────────────────────
FIXED_CATEGORIES = {
    "liaos_writings": "廖耀湘文集",
    "liaos_tele": "Liao's Tele",
    "newspapers": "报刊杂志",
}


# ── parse the issue body ────────────────────────────────────────────
def parse_issue_body(body: str) -> dict:
    """GitHub issue forms produce ``### Label\\n\\nValue\\n\\n`` blocks."""
    fields: dict[str, str] = {}
    current_key: str | None = None
    buf: list[str] = []

    for line in body.splitlines():
        if line.startswith("### "):
            if current_key is not None:
                fields[current_key] = "\n".join(buf).strip()
            current_key = line[4:].strip()
            buf = []
        else:
            buf.append(line)

    if current_key is not None:
        fields[current_key] = "\n".join(buf).strip()

    # Normalise keys coming from the issue template
    mapping = {
        "Collection / 文集": "collection",
        "Battles subfolder / 战史子目录": "battles_subfolder",
        "Title / 标题": "title",
        "Author / 作者": "author",
        "Category / 分类": "category",
        "Date / 日期": "date",
        "Source / 来源": "source",
        "Transcriber / 录入校对": "transcriber",
        "Add TOC / 添加目录": "toc",
        "Content / 文章内容": "content",
        "Notes / 备注": "notes",
    }

    parsed: dict[str, str] = {}
    for label, key in mapping.items():
        parsed[key] = fields.get(label, "").strip()

    return parsed


def resolve_collection(raw: str) -> str:
    """``"liaos_tele (来往电报)"`` → ``"liaos_tele"``."""
    return raw.split("(")[0].strip().split()[0].strip()


# ── Claude API call ─────────────────────────────────────────────────
SYSTEM_PROMPT = """\
你是一个历史文献排版助手。你的唯一任务是将用户提供的原始文章文本转换为格式规范的 Markdown 正文内容。

严格规则（必须遵守）：
1. **绝不输出 YAML frontmatter**（即 `---` 块）。你只输出正文 Markdown。
2. **绝不修改、删除或改写历史原文内容。** 保持每一个字、每一个标点完全不变。
3. **保留中文标点**（全角句号、逗号、引号等），不要替换为英文标点。
4. 不要添加任何你自己的评论、注释、说明或总结。

排版规范：
- 使用 Markdown 标题（### 三级标题）来标记文章中明显的章节划分。
- 段落之间用空行分隔。
- 诗句每行末尾添加 `<br>` 标签以保持换行，诗节之间用空行分隔。
- 如果原文有编号列表，使用 Markdown 编号列表格式。

集合特定规则：
- 对于 liaos_writings（廖耀湘文集）和 liaos_tele（来往电报）：不要在正文开头添加作者行（"> 作者名"）。
- 对于其他集合（newspapers, ten_year_memorial, n6a_memorial, n22d_memorial, battles_history）：在正文第一行添加 `> 作者名`（使用 blockquote 格式），然后空一行再开始正文。

页脚格式（按顺序，放在文章末尾）：
{footer_instructions}

TOC 规则：
{toc_instructions}

请直接输出格式化后的 Markdown 正文，不要包含任何前言或后语。"""

FOOTER_WITH_BOTH = """\
- 如果有录入校对信息，在正文最后添加：`> *录入校对：{transcriber}*`
- 如果有来源信息，在正文最后添加：`> 来源：{source}`
- 录入校对行在前，来源行在后，各占一行，之间用空行分隔。"""

FOOTER_TRANSCRIBER_ONLY = """\
- 在正文最后添加：`> *录入校对：{transcriber}*`"""

FOOTER_SOURCE_ONLY = """\
- 在正文最后添加：`> 来源：{source}`"""

FOOTER_NONE = """\
- 不需要添加页脚。"""

TOC_YES = """\
- 在正文开头（作者行之后，如果有的话）插入以下两行：
```
* TOC
{:toc}
```
然后空一行再开始正文内容。"""

TOC_NO = """\
- 不添加目录。"""


def build_system_prompt(data: dict) -> str:
    # Footer instructions
    has_source = bool(data.get("source"))
    has_transcriber = bool(data.get("transcriber"))
    if has_source and has_transcriber:
        footer = FOOTER_WITH_BOTH.format(
            transcriber=data["transcriber"], source=data["source"]
        )
    elif has_transcriber:
        footer = FOOTER_TRANSCRIBER_ONLY.format(transcriber=data["transcriber"])
    elif has_source:
        footer = FOOTER_SOURCE_ONLY.format(source=data["source"])
    else:
        footer = FOOTER_NONE

    # TOC instructions
    toc = TOC_YES if data.get("toc", "").lower() == "yes" else TOC_NO

    return SYSTEM_PROMPT.format(
        footer_instructions=footer,
        toc_instructions=toc,
    )


def call_claude(data: dict) -> str:
    """Send the raw content to Claude and return formatted markdown body."""
    client = anthropic.Anthropic()

    collection = resolve_collection(data["collection"])
    user_message = (
        f"集合：{collection}\n"
        f"标题：{data['title']}\n"
        f"作者：{data['author']}\n"
    )
    if data.get("notes"):
        user_message += f"特殊说明：{data['notes']}\n"
    user_message += f"\n---\n\n{data['content']}"

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16000,
        system=build_system_prompt(data),
        messages=[{"role": "user", "content": user_message}],
    )

    return message.content[0].text


# ── generate frontmatter (deterministic) ────────────────────────────
def generate_frontmatter(data: dict) -> str:
    collection = resolve_collection(data["collection"])
    category = FIXED_CATEGORIES.get(collection, data["category"])
    title_escaped = data["title"].replace('"', '\\"')
    author_escaped = data["author"].replace('"', '\\"')
    category_escaped = category.replace('"', '\\"')
    article_date = data.get("date", "1900-01-01").strip()

    return (
        f'---\n'
        f'layout: post\n'
        f'title: "{title_escaped}"\n'
        f'author: "{author_escaped}"\n'
        f'category: "{category_escaped}"\n'
        f'tags: 分类\n'
        f'date: {article_date} 00:00:00 +0000\n'
        f'---\n'
    )


# ── determine file path ────────────────────────────────────────────
def determine_file_path(data: dict) -> Path:
    collection = resolve_collection(data["collection"])
    title = data["title"].strip()
    author = data["author"].strip()
    article_date = data.get("date", "1900-01-01").strip()

    if collection == "liaos_tele":
        # Format: YYYY-MM-DDTitle.md
        filename = f"{article_date}{title}.md"
        return DOCS / "_liaos_tele" / filename

    if collection == "battles_history":
        subfolder = data.get("battles_subfolder", "N/A").strip()
        if not subfolder or subfolder == "N/A":
            subfolder = "1939"  # fallback
        if author:
            filename = f"{title}（{author}）.md"
        else:
            filename = f"{title}.md"
        return DOCS / "_battles_history" / subfolder / filename

    # All other collections: docs/_{collection}/Title（Author）.md
    if author:
        filename = f"{title}（{author}）.md"
    else:
        filename = f"{title}.md"
    return DOCS / f"_{collection}" / filename


# ── update changelog ────────────────────────────────────────────────
def determine_url(file_path: Path) -> str:
    """Derive the Jekyll URL from the file path.

    Examples:
        docs/_liaos_tele/1937-09-02xxx.md  →  /liaos_tele/1937-09-02xxx.html
        docs/_battles_history/1939/foo.md  →  /battles_history/1939/foo.html
        docs/_ten_year_memorial/bar.md     →  /ten_year_memorial/bar.html
    """
    rel = file_path.relative_to(DOCS)
    parts = list(rel.parts)
    # Strip leading underscore from collection dir name
    parts[0] = parts[0].lstrip("_")
    # Replace .md with .html
    parts[-1] = re.sub(r"\.md$", ".html", parts[-1])
    return "/" + "/".join(parts)


def update_changelog(title: str, url: str) -> None:
    """Prepend a new entry (or append to today's entry) in changelog.yml.

    Uses manual string building to preserve the existing formatting style
    rather than yaml.dump which would alter quoting/indentation.
    """
    today = date.today().isoformat()  # YYYY-MM-DD

    existing = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else ""

    # Check if the first entry is already for today
    first_date_match = re.match(r"- date: (\S+)", existing)
    if first_date_match and first_date_match.group(1) == today:
        # Append to the existing first entry's changes list
        # Find the end of the `changes:` block for the first entry
        # We look for the next `- date:` or end-of-file
        # Insert our new change line before that boundary
        lines = existing.split("\n")
        insert_idx = None
        in_first_entry = True
        for i, line in enumerate(lines):
            if i == 0:
                continue
            if line.startswith("- date:"):
                insert_idx = i
                break
        if insert_idx is None:
            insert_idx = len(lines)
            # Remove trailing empty lines
            while insert_idx > 0 and lines[insert_idx - 1].strip() == "":
                insert_idx -= 1

        new_change = f'    - title: "{title}"\n      url: "{url}"'
        lines.insert(insert_idx, new_change)
        updated = "\n".join(lines)
    else:
        # Prepend a brand-new entry
        new_entry = (
            f"- date: {today}\n"
            f'  commit_message: "+ 1 新文章"\n'
            f"  changes:\n"
            f'    - title: "{title}"\n'
            f'      url: "{url}"\n'
        )
        updated = new_entry + existing

    CHANGELOG.write_text(updated, encoding="utf-8")


# ── main ────────────────────────────────────────────────────────────
def main() -> None:
    issue_body = os.environ.get("ISSUE_BODY", "")
    if not issue_body:
        print("ERROR: ISSUE_BODY environment variable is empty.", file=sys.stderr)
        sys.exit(1)

    data = parse_issue_body(issue_body)

    # Validate required fields
    for field in ("collection", "title", "author", "category", "date", "content"):
        if not data.get(field):
            print(f"ERROR: Missing required field: {field}", file=sys.stderr)
            sys.exit(1)

    # Auto-correct category for fixed collections
    collection = resolve_collection(data["collection"])
    if collection in FIXED_CATEGORIES:
        data["category"] = FIXED_CATEGORIES[collection]

    print(f"Processing article: {data['title']}")
    print(f"Collection: {collection}")
    print(f"Author: {data['author']}")

    # Call Claude API to format the body
    print("Calling Claude API to format article content...")
    formatted_body = call_claude(data)

    # Generate frontmatter deterministically
    frontmatter = generate_frontmatter(data)

    # Combine into full markdown
    full_content = frontmatter + "\n" + formatted_body + "\n"

    # Determine file path and write
    file_path = determine_file_path(data)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(full_content, encoding="utf-8")
    print(f"Article written to: {file_path.relative_to(REPO_ROOT)}")

    # Update changelog
    title_for_changelog = data["title"]
    if data["author"] and collection not in ("liaos_tele",):
        title_for_changelog = f"{data['title']}（{data['author']}）"
    url = determine_url(file_path)
    update_changelog(title_for_changelog, url)
    print(f"Changelog updated with URL: {url}")

    # Write outputs for the workflow
    github_output = os.environ.get("GITHUB_OUTPUT", "")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"article_path={file_path.relative_to(REPO_ROOT)}\n")
            f.write(f"article_title={data['title']}\n")


if __name__ == "__main__":
    main()
