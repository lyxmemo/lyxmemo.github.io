Process raw newspaper text and add it to the lyxmemo site. The user will provide raw text from a historical newspaper article.

## Steps

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

## IMPORTANT: YAML quoting pitfall

When editing `chronology.yml`, the Edit tool may silently convert straight quotes (`"`, U+0022) to curly/smart quotes (`""`, U+201C/U+201D). YAML only recognizes straight quotes as string delimiters — curly quotes become part of the literal value, breaking date parsing and display.

**After every edit to chronology.yml**, validate with:
```bash
ruby -ryaml -rdate -e 'data = YAML.safe_load(File.read("docs/_data/chronology.yml"), permitted_classes: [Date]); puts "OK"'
```

If entries show `""` as date badges or content wrapped in literal quotes on the site, check for curly quotes and replace them with straight quotes using a Ruby/Python script (the Edit tool cannot reliably fix this since it may re-introduce curly quotes).

Also: never put long text with internal straight `"` characters inside a double-quoted YAML value — the parser will see the internal `"` as the end of the string. Use `original_text: ""` and store the full text in the separate newspaper file instead.

## Format for chronology entry
```yaml
    - date: "YYYY-MM-DD"
      date_display: ""
      content: "<short summary in simplified Chinese>"
      source: "申报 YYYY年MM月DD日 第X版 第XXXXX期"
      source_url: "/newspapers/<headline>.html"
      original_text: ""
      notes: ""
```

$ARGUMENTS
