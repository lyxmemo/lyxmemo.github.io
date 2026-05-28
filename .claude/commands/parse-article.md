Read the user-provided article text, extract metadata, and output the `commit-article.sh --batch` command. This is "Step 0" — run this BEFORE add-newspaper.

## What to do

1. Read the article text the user provided (in $ARGUMENTS or in the conversation). Read it 100 lines at a time. Most lines are body content — skim them and focus on extracting metadata from the beginning and end of the text.

2. Extract these fields:
   - **TITLE**: The article's title/headline (usually the first line)
   - **AUTHOR**: The writer. Look for author name at the top (after title), or at the end with `*作者当时系…*` pattern. For newspapers, the author is the newspaper name (e.g. 申报, 中央日报)
   - **COLLECTION**: One of: `newspapers`, `battles_history`, `liaos_writings`, `liaos_tele`, `n6a_memorial`, `n22d_memorial`, `ten_year_memorial`
   - **SUBFOLDER** (battles_history only): e.g. `liaoshen/1948`, `1944`, etc.
   - **CATEGORY**: For newspapers=`报刊杂志`, liaos_writings=`廖耀湘文集`, liaos_tele=`Liao's Tele`. For 文史资料 articles=`文史资料`. For memorial collections, use the publication name.
   - **DATE**: Event date in YYYY-MM-DD. Use the primary event date, not publication date. If only year known, use YYYY-01-01.
   - **SOURCE**: Publication info. e.g. `文史资料存稿选编-全面内战（中）`, `申报 1945年09月06日 第1版 第25659期`
   - **TRANSCRIBER**: Default `观棋不语` unless specified
   - **TOC**: `y` if article has multiple `##` section headers, `n` otherwise

3. **Output the results to the user** in this exact format:

```
Metadata extracted:
- TITLE: ...
- AUTHOR: ...
- COLLECTION: ...
- SUBFOLDER: ... (or N/A)
- CATEGORY: ...
- DATE: ...
- SOURCE: ...
- TOC: y/n

Ready to run:
```

Then output the bash command:

```bash
ARTICLE_FILE=/tmp/article.txt \
COLLECTION=... \
SUBFOLDER=... \
TITLE="..." \
AUTHOR="..." \
CATEGORY="..." \
DATE=... \
SOURCE="..." \
TRANSCRIBER="观棋不语" \
TOC=n \
COMMIT=n \
PUSH=n \
bash commit-article.sh --batch
```

4. **Save the article content** (the raw body text without metadata lines like `*作者当时系…*` or `来源：...` that are already captured in SOURCE) to `/tmp/article.txt`

5. **Ask the user** to confirm or adjust the metadata before running the command.

## Important

- Do NOT read any other files. You have everything you need from the article text itself.
- Do NOT read chronology.yml or any existing site files.
- Output progress as you read so the user knows you're not stuck.
- Set COMMIT=n so the user can review the file before committing.

$ARGUMENTS
