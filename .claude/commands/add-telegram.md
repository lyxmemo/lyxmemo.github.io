Process raw telegram text and add it to the lyxmemo site. The user will provide the raw text of a historical telegram (电报/电文), possibly including metadata from the physical telegraph form.

## Input

The user provides:
- The **raw telegram text**, which may include:
  - A traditional Chinese title (e.g. "廖耀湘電何應欽轉蔣中正告以與史迪威會議後指揮權之變動情形")
  - Telegraph form metadata (来电纸/去电录底纸/发电纸 headers, 号次, 发往地点, etc.)
  - The telegram body
  - Signature/closing (e.g. "职廖耀湘叩申齐辰霞印")
  - Transcriber credit (录入校对)
  - Footnotes or annotations
- Optionally, source information (e.g. "国史馆", archive link)

## Step 1: Parse the telegram

Extract the following from the raw text:

1. **Title**: The traditional Chinese title describing the telegram (e.g. "廖耀湘電何應欽轉蔣中正告以與史迪威會議後指揮權之變動情形"). Convert to simplified Chinese for the filename.
2. **Date**: Convert from 民国 dating (e.g. "33年9月8日" = 1944-09-08) or extract from the text. 民国 year + 1911 = Western year.
3. **Sender and recipients**: Identify from the title or body.
4. **Telegraph form metadata**: If present, preserve headers like "国民政府军事委员会办公厅机要室", "来电纸", "号次", dates, etc.
5. **Body text**: The main telegram content.
6. **Footnotes/annotations**: Any `*` markers, 校对注, numbered footnotes, etc.
7. **录入校对 credit**: The transcriber name.
8. **批复/批示**: Any response annotations appended to the telegram.

## Step 2: Check for existing file

Search for an existing file in `docs/_liaos_tele/` matching the date and title:
```bash
ls docs/_liaos_tele/YYYY-MM-DD*.md
```

- If a **stub file** exists (title contains `[待录入]` or `[已认领待录入]`), update it in place
- If **no file** exists, create a new one

## Step 3: Create or update the telegram file

**Filename**: `docs/_liaos_tele/YYYY-MM-DD<simplified-Chinese-title>.md`

The filename title should use simplified Chinese and follow the pattern: `<sender>电/呈/致<recipient><brief-description>`

**Frontmatter**:
```yaml
---
layout: post
title: "YYYY/MM/DD<simplified-title>"
author: "电文"
category: "Liao's Tele"
tags: 分类
date: YYYY-MM-DD 00:00:00 +0000
---
```

**Body content** — assemble in this order:

1. **Telegraph form metadata** (if provided): Preserve lines like "国民政府军事委员会办公厅机要室", "来电纸", "号次 XXXXX", date/time info, destination, etc. Omit these if the user did not provide them.

2. **Telegram body text**: Preserve original formatting and punctuation. Break the body into logical paragraphs — the raw text from the user is often a continuous block, but should be segmented at natural topic boundaries (e.g. separate the opening address, each distinct topic/request, and the closing signature into their own paragraphs). Each paragraph should be separated by a blank line.

3. **Footnotes/annotations**: Format with `\*` for single footnotes or numbered footnotes as appropriate. Place after the main body with a blank line separator. Use proper Chinese quotation marks `\u201c\u201d` (not straight ASCII `"`) in body text and footnotes — e.g. `\*意同\u201c不卑不亢\u201d。` Since the Write/Edit tools may not reliably produce these, use a python script to replace straight `"` pairs in the body text with `\u201c`/`\u201d` after writing the file.

4. **录入校对 credit**: Format as `>*录入校对：<name>*` on its own line, preceded by a blank line.

5. **Source attribution**: Format as:
   - With archive link: `> 来源：国史馆 [*原档链接：<traditional-Chinese-title>*](<URL>)`
   - Without link: `> 来源：国史馆 [*原档链接：（暂缺，可于国史馆网站搜索"<traditional-Chinese-title>"）*]()`
   - Other sources: `> 来源：<source description>`

## Step 4: Update the chronology

Edit `docs/_data/chronology.yml` to add or update the entry for this date.

**IMPORTANT**: The chronology file is very long. Do NOT read the entire file. Instead:
1. Use `grep -n` to search for the date (YYYY-MM-DD) to find existing entries
2. If updating an existing entry, read only the surrounding lines (use offset/limit) and edit
3. If adding a new entry, find the correct insertion point by searching for adjacent dates

**For existing entries**: Update the `content` field with a richer summary based on the actual telegram text. If the entry was a placeholder, expand it with specific details from the telegram.

**For new entries**: Insert in chronological order within the correct year block:
```yaml
  - "date": "YYYY-MM-DD"
    "date_display": ""
    "content": "<1-2 sentence summary in simplified Chinese, focused on what happened>"
    "source": "<simplified-Chinese-title>"
    "source_url": "/liaos_tele/YYYY-MM-DD<simplified-Chinese-title>.html"
    "original_text": ""
    "notes": ""
```

The `content` should be a concise summary (1-2 sentences) of the telegram's substance, written in simplified Chinese. Focus on the key events, decisions, or information reported — not just "sent a telegram about X" but the actual content (e.g. "偕孙立人在利多与史迪威会议，获赋指挥作战、教育、人事、经理全权").

## Step 5: Validate

After editing `chronology.yml`, validate YAML:
```bash
ruby -ryaml -rdate -e 'data = YAML.safe_load(File.read("docs/_data/chronology.yml"), permitted_classes: [Date]); puts "OK"'
```

## Quote safety rules

**CRITICAL**: The Edit and Write tools may silently convert straight quotes (`"`, U+0022) to curly/smart quotes (`""`, U+201C/U+201D). This breaks YAML and corrupts frontmatter.

**For the telegram `.md` file**: After writing/editing, always verify no curly quotes were introduced:
```bash
python3 -c "
content = open('<filepath>', 'rb').read()
for i, b in enumerate(content):
    if b == 0xe2:
        t = content[i:i+3]
        if t in (b'\xe2\x80\x9c', b'\xe2\x80\x9d'):
            print(f'Curly quote at byte {i}, line {content[:i].count(b\"\\n\")+1}')
print('Done')
"
```
If curly quotes are found, fix them:
```bash
python3 -c "
c = open('<filepath>','r').read().replace('\u201c','\"').replace('\u201d','\"')
open('<filepath>','w').write(c)
"
```

**For `chronology.yml`**: Same curly quote risk applies. After every edit, validate:
```bash
ruby -ryaml -rdate -e 'data = YAML.safe_load(File.read("docs/_data/chronology.yml"), permitted_classes: [Date]); puts "OK"'
```
- Never put text containing internal `"` characters inside a double-quoted YAML value.
- If validation fails, check for curly quotes and fix them.

## Step 6: Summary

Report to the user:
- Whether the file was created new or updated from a stub
- The file path
- What was added/changed in the chronology
- YAML validation result

$ARGUMENTS
