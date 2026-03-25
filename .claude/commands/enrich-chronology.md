Enrich the chronology (年谱) from a pure text article that is already on the site or provided as raw text. Extract all datable events related to 廖耀湘, 新二十二师/新22师, or 新六军/新6军, and add or update entries in `docs/_data/chronology.yml`.

## Input

The user provides either:
- A **file path** to an existing article on the site (e.g. a `.md` file under `docs/`)
- A **raw text** block from a historical source (memoir, war history, official account)

## Step 1: Read and analyze the source

1. Read the full text carefully
2. Extract **every event with a specific date** (year-month-day, year-month, or at minimum year) that mentions 廖耀湘, 新22师/新二十二师, 新6军/新六军/新编第六军, or units/people directly under their command
3. For each event, note:
   - **Date**: as precise as possible (YYYY-MM-DD preferred; YYYY-MM or YYYY if that's all available)
   - **Summary**: 1-2 sentence description in simplified Chinese, focused on what 廖耀湘 or his units did
   - **Original quote**: the key sentence(s) from the source that support this entry
   - **Source name**: author and title of the article

## Step 2: Compare with existing chronology

1. Read `docs/_data/chronology.yml`
2. For each extracted event, check if a matching entry already exists:
   - **Same event, same date** → update: add this source to `source` and `source_url` (semicolon-separated) as corroboration
   - **Same event, different date** → add a note about the date discrepancy
   - **New event** → add a new entry

## Step 3: Edit chronology.yml

For **new entries**, insert in chronological order within the correct year block:
```yaml
    - date: "YYYY-MM-DD"
      date_display: ""
      content: "<short summary>"
      source: "<source name>"
      source_url: "<path to .html file on site, or empty>"
      original_text: "<key quote from source>"
      notes: ""
```

For **corroboration of existing entries**, append to `source` and `source_url` with `; ` separator:
```yaml
      source: "existing source; new source"
      source_url: "existing_url; new_url"
```

If the original_text field of the existing entry is empty, fill it in with a relevant quote.

## Rules

- Entries are grouped by `year:` blocks and sorted chronologically within each block
- If a year block doesn't exist yet, create one in the right position
- `date_display` is only used when the display format differs from YYYY-MM-DD (e.g. "1944年春" for approximate dates)
- For approximate dates, set `date` to the best estimate (e.g. "1944-03" for spring 1944) and `date_display` to the descriptive text
- `content` should be concise (1-2 sentences), in simplified Chinese, and focused on 廖耀湘 or his units
- `original_text` should contain the most relevant direct quote — keep it short (1-2 sentences). If the quote contains internal `"` characters, leave `original_text: ""` to avoid YAML parsing issues
- `notes` is for editorial commentary: date discrepancies, cross-references, corrections, etc.
- Do NOT duplicate existing entries — always check first

## YAML safety

After every edit to `chronology.yml`, validate:
```bash
ruby -ryaml -rdate -e 'data = YAML.safe_load(File.read("docs/_data/chronology.yml"), permitted_classes: [Date]); puts "OK: #{data.size} years"'
```

Watch for:
- Curly/smart quotes (`""`) — YAML only accepts straight quotes (`"`)
- Internal straight `"` inside double-quoted values — will break parsing
- Missing fields — every entry must have all 7 fields

## Step 4: Summary

After editing, provide a summary listing:
- Number of new entries added
- Number of existing entries updated with new source
- Any date discrepancies found

$ARGUMENTS
