Enrich the chronology (年谱) from a pure text article that is already on the site or provided as raw text.

**CRITICAL: The chronology file is 4000+ lines. NEVER read the entire file. Use targeted Grep searches to find insertion points.**

## Input

The user provides either:
- A **file path** to an existing article on the site (e.g. a `.md` file under `docs/`)
- A **raw text** block from a historical source

## Step 1: Read the article (50 lines at a time)

Read the source text **50 lines at a time**. For each chunk, extract events that meet ALL of these conditions:
- A **date** is present or can be clearly inferred (year-month-day, year-month, or at minimum year)
- The event is related to **廖耀湘**, **新六军**（新6军）, **新二二师**（新二十二师，新22师，新廿二师）, or **十四师**

For each qualifying event, note:
- **Date**: YYYY-MM-DD (or YYYY-MM, YYYY if less precise)
- **Event summary**: 1-2 sentences in simplified Chinese
- **Source**: author and title

## Step 2: List extracted events

**Before touching chronology.yml**, list all (date, event) pairs in your response for the user to review. Wait for confirmation if the user is present, or proceed if running autonomously.

## Step 3: Insert into chronology.yml using targeted search

For EACH event:

1. **Grep for the year**: `Grep` pattern `year: <YYYY>` in `docs/_data/chronology.yml` to find the line number
2. **Grep for nearby dates**: `Grep` pattern `date: "<YYYY-MM` in `docs/_data/chronology.yml` to find entries in the same month
3. **Read only 50-100 lines** around the match to find the exact insertion point
4. **Check for duplicates**: If an existing entry covers the same event, update its `source` and `source_url` (semicolon-separated) instead of adding a new one
5. **Insert** the new entry using Edit tool

Entry format:
```yaml
    - date: "YYYY-MM-DD"
      date_display: ""
      content: "<short summary>"
      source: "<source name>"
      source_url: "<path to .html file on site, or empty>"
      original_text: ""
      notes: ""
```

### Rules for entries
- `date_display`: only used when display differs from YYYY-MM-DD (e.g. "1944年春")
- For approximate dates: `date` = best estimate, `date_display` = descriptive text
- `content`: concise, simplified Chinese, focused on 廖耀湘 or his units
- `original_text`: leave as `""` to avoid YAML quoting issues
- `notes`: for date discrepancies or cross-references

## Step 4: Validate YAML (once, after all edits)

```bash
ruby -ryaml -rdate -e 'data = YAML.safe_load(File.read("docs/_data/chronology.yml"), permitted_classes: [Date]); puts "OK: #{data.size} years"'
```

Watch for curly/smart quotes (`""`) — YAML only accepts straight quotes (`"`).

## Step 5: Summary

List:
- Number of new entries added
- Number of existing entries updated
- Any date discrepancies found

$ARGUMENTS
