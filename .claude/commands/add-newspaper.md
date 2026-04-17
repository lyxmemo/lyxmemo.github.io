Process raw text and add it to the lyxmemo site. The user will provide raw text from a historical newspaper article or a historical article/memoir (e.g. from 文史资料).

## Step 0: Parse the article first

Run `/parse-article` with the user's text. This reads the article, extracts metadata (title, author, collection, date, source, etc.), and outputs the ready-to-run `commit-article.sh --batch` command. The user confirms or adjusts metadata before proceeding.

## Step 1: Run commit-article.sh in batch mode

After Step 0 produces the command, run it. The script creates the file directly and commits — no interactive prompts.

### Batch mode syntax:

```bash
ARTICLE_FILE=/tmp/article.txt \
COLLECTION=battles_history \
SUBFOLDER=liaoshen/1948 \
TITLE="文章标题" \
AUTHOR="作者" \
CATEGORY="文史资料" \
DATE=1948-10-31 \
SOURCE="来源出版物" \
TRANSCRIBER="观棋不语" \
TOC=n \
COMMIT=y \
PUSH=n \
bash commit-article.sh --batch
```

### Determining metadata values:

- **COLLECTION**: One of: `newspapers`, `battles_history`, `liaos_writings`, `liaos_tele`, `n6a_memorial`, `n22d_memorial`, `ten_year_memorial`
- **SUBFOLDER** (battles_history only): `1939`, `1942`, `1943`, `1944`, `1945`, `liaoshen/1946`, `liaoshen/1947`, `liaoshen/1948`
- **TITLE**: Extract from the text (first line or heading)
- **AUTHOR**: For newspapers = newspaper name (e.g. 申报); for articles = author's name
- **CATEGORY**: Auto-set for newspapers (报刊杂志), liaos_writings (廖耀湘文集), liaos_tele (Liao's Tele). For others, set manually (e.g. 文史资料)
- **DATE**: Event date in YYYY-MM-DD format
- **SOURCE**: Publication info
- **TOC**: `y` for long multi-section articles, `n` for short pieces
- **COMMIT**: `y` to auto-commit, `n` to skip
- **PUSH**: `y` to auto-push, `n` to skip

## After the file is created

Tell the user the file path and commit hash. Ask if they want to push.

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
