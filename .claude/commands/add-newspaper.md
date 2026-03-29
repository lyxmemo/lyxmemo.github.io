Process raw text and add it to the lyxmemo site. The user will provide raw text from a historical newspaper article or a historical article/memoir (e.g. from 文史资料).

## CRITICAL: Use the add-article.sh script

For adding ANY article (newspaper or memoir), **always use the `add-article.sh` script** at the repo root. This script creates a GitHub issue with proper metadata, which triggers automated PR generation.

### How to use it:

1. **Save the user's raw text to a temp file** (e.g. `/tmp/article.txt`)
2. **Run the script interactively**: `bash add-article.sh /tmp/article.txt`
3. The script will prompt for collection, title, author, date, etc. — answer based on the parsed content.

### Determining answers for the prompts:

- **Collection**: Pick based on content type:
  - Newspaper clippings → `3` (newspapers/报刊杂志)
  - Battle histories/memoirs → `7` (battles_history/战史)
  - 廖耀湘's own writings → `1` (liaos_writings/廖耀湘文集)
  - Telegrams → `2` (liaos_tele/来往电报)
  - 新六军 memorial articles → `4` (n6a_memorial/新六军纪念)
  - 新二十二师 memorial articles → `5` (n22d_memorial/新二十二师纪念)
  - Retrospective memoirs by others → `6` (ten_year_memorial/故人回忆)
- **Battles subfolder** (if battles_history): pick the year of the events described
- **Title**: Extract from the text (first line or heading)
- **Author**: For newspapers, use the newspaper name (e.g. 申报); for articles, use the author's name
- **Date**: The event date in YYYY-MM-DD format
- **Source**: Publication info (e.g. "申报 1945年09月06日 第1版")
- **Transcriber**: Default is 观棋不语 unless user specifies otherwise
- **TOC**: Y for long multi-section articles, N for short pieces
- **Notes**: Any relevant notes

## After the issue is created

Tell the user the issue URL and that a PR will be auto-generated.

## Updating the chronology (if requested)

If the user also wants to update the chronology, follow the steps below. **Do NOT read the entire chronology file** — it is 4000+ lines and will cause timeouts.

### Step 1: Read the article (50 lines at a time)

Read through the provided article text, 50 lines at a time. For each chunk, note:
- **Date** (must be present or clearly inferable from context)
- **Event** (what happened)
- Only record events related to: 廖耀湘, 新六军（新6军）, 新二二师（新二十二师，新22师，新廿二师）, or 十四师

Skip events where no date can be determined.

### Step 2: Write down extracted events

Before touching chronology.yml, list all extracted (date, event) pairs in your response so the user can verify.

### Step 3: Insert into chronology.yml using targeted search

For each event to add:

1. **Search for the year block**: Use `Grep` to find `year: <YYYY>` in `docs/_data/chronology.yml`
2. **Search for the month** (if known): Use `Grep` to find `date: "<YYYY-MM` near that year block
3. **Read only the relevant section** (50-100 lines around the match) to find the exact insertion point
4. **Insert the new entry** or update an existing one using the Edit tool

Entry format:
```yaml
    - date: "YYYY-MM-DD"
      date_display: ""
      content: "<short summary in simplified Chinese>"
      source: "<source name>"
      source_url: "<path to .html file>"
      original_text: ""
      notes: ""
```

### YAML safety

After ALL edits are done (not after each edit), validate once:
```bash
ruby -ryaml -rdate -e 'data = YAML.safe_load(File.read("docs/_data/chronology.yml"), permitted_classes: [Date]); puts "OK: #{data.size} years"'
```

Watch for curly/smart quotes — YAML only accepts straight quotes (`"`).

$ARGUMENTS
