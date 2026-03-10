## Prerequisites

In `docs/`:

```
npm install puppeteer --legacy-peer-deps
```

## Steps

In `docs/`:

1. Build the Jekyll site:
```
bundle exec jekyll build
```

2. Run the generate script (generates PDF + TXT):
```
bash utils/generate-book.sh
```

Or run steps manually:

### PDF (via Puppeteer)
```
node utils/generate_pdf.js _site/book.html assets/与廖耀湘有关的文字资料合集.pdf
```

### TXT
```
python3 -c "import re; html = open('_site/book.html').read(); clean = re.sub('<[^<]+?>', '', html); print('\n'.join(line.strip() for line in clean.splitlines() if line.strip()))" > assets/与廖耀湘有关的文字资料合集.txt
```

## Deprecated

- weasyprint — replaced by Puppeteer for PDF generation
- EPUB — no longer served
