Process raw text and add it to the lyxmemo site. The user will provide raw text from a historical newspaper article or a historical article/memoir (e.g. from 文史资料).

## Determine the content type

- **Newspaper**: Short news clippings from 申报, 中央日报, etc. with publication info (date, page, issue number)
- **Article/Memoir**: Longer pieces from collections like 文史资料存稿选编, 文史资料选辑, etc. Often written by military participants with reviewer (审稿) comments. May include author info like "*作者当时系…*"

## Steps for Newspapers

1. **Parse the raw text** to extract:
   - Headline/title (first line(s) before the body)
   - Article body (the full text)
   - Publication info (date, page, issue number — usually at the end, e.g. "1945年09月06日 第1版 第25659期")
   - Event date(s) mentioned in the article (e.g. "南京五日電" means the 5th of that month)
   - The newspaper source is 申报 unless explicitly stated otherwise

2. **Create a newspaper file** at `docs/_newspapers/<headline>.md` with:
   ```
   ---
   layout: post
   title: "<full headline>"
   author: "申报"
   category: "报刊杂志"
   tags: 分类
   date:  <publication-date> 00:00:00 +0000
   ---

   > 申报 <publication-date> 第X版 第XXXXX期

   <article body, preserving original formatting and punctuation>

   > 申报 <publication-date> 第X版 第XXXXX期
   ```

3. **Add a chronology entry** in `docs/_data/chronology.yml`:
   - Find the correct position by date (entries are sorted chronologically within each year)
   - The entry date should be the **event date** from the article content, not the publication date
   - Write a **short summary** (1-2 sentences) focused on 新六军 or 廖耀湘
   - Include all 7 fields: `date`, `date_display`, `content`, `source`, `source_url`, `original_text`, `notes`
   - Set `source` to the publication info (e.g. "申报 1945年09月06日 第1版 第25659期")
   - Set `source_url` to `/newspapers/<headline>.html`
   - If an existing chronology entry already covers the same event, **update its `source_url`** instead of creating a duplicate

## Steps for Articles/Memoirs

1. **Parse the raw text** to extract:
   - Title (may include 节选 if excerpted)
   - Author name(s)
   - Source publication (e.g. 文史资料存稿选编——全面内战（上）)
   - Event date(s) — the historical period the article describes
   - Reviewer (审稿) comments if any
   - Author bio line (e.g. "*作者当时系…*")

2. **Determine the destination folder** based on content:
   - Articles about battles/campaigns in the Chinese Civil War in Northeast China (1946-1948) go to `docs/_battles_history/liaoshen/<year>/`
   - Articles about anti-Japanese War battles (1939-1945) go to `docs/_battles_history/<year>/`
   - The `<year>` is determined by the primary events described, not the writing date
   - Look at existing files in the target folder for format reference

3. **Create the article file** at `docs/_battles_history/.../<title>（<author>）.md` with:
   ```
   ---
   layout: post
   title: "<title>"
   author: "<author>"
   category: "<source publication short name, e.g. 文史资料存稿选编>"
   tags: 分类
   date: <event-date> 00:00:00 +0000
   ---

   > <author>

   录入校对：观棋不语

   <reviewer comments if any>

   <article body, preserving original formatting and punctuation>

   <author bio line>

   > 来源：<full source publication name>
   ```

4. **Add a chronology entry** in `docs/_data/chronology.yml` (same rules as newspapers):
   - Set `source` to the source publication name
   - Set `source_url` to the article's URL path (e.g. `/battles_history/liaoshen/1947/<filename>.html`)

## IMPORTANT: YAML quoting pitfall

When editing `chronology.yml`, the Edit tool may silently convert straight quotes (`"`, U+0022) to curly/smart quotes (`""`, U+201C/U+201D). YAML only recognizes straight quotes as string delimiters — curly quotes become part of the literal value, breaking date parsing and display.

**After every edit to chronology.yml**, validate with:
```bash
ruby -ryaml -rdate -e 'data = YAML.safe_load(File.read("docs/_data/chronology.yml"), permitted_classes: [Date]); puts "OK"'
```

If entries show `""` as date badges or content wrapped in literal quotes on the site, check for curly quotes and replace them with straight quotes using a Ruby/Python script (the Edit tool cannot reliably fix this since it may re-introduce curly quotes).

Also: never put long text with internal straight `"` characters inside a double-quoted YAML value — the parser will see the internal `"` as the end of the string. Use `original_text: ""` and store the full text in the separate file instead.

## Format for chronology entry
```yaml
    - date: "YYYY-MM-DD"
      date_display: ""
      content: "<short summary in simplified Chinese>"
      source: "<source publication>"
      source_url: "<path to .html file>"
      original_text: ""
      notes: ""
```

$ARGUMENTS
