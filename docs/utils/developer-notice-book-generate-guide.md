# 📚 Book Generation Guide

## Prerequisites

In the `docs/` directory, run Jekyll to build static HTML:

```bash
bundle exec jekyll serve
```

This generates `_site/book.html` which is used for all conversions.

## Quick Start

Run the automated script to generate all formats:

```bash
cd docs/utils
./generate-book.sh
```

This creates:
- `assets/与廖耀湘有关的文字资料合集.pdf` (Node.js + Puppeteer)
- `assets/与廖耀湘有关的文字资料合集.epub` (if Pandoc installed)
- `assets/与廖耀湘有关的文字资料合集.txt` (Python)

---

## Manual Commands

### PDF Generation (Node.js + Puppeteer)

```bash
cd docs
npm install puppeteer
node utils/generate_pdf.js _site/book.html assets/与廖耀湘有关的文字资料合集.pdf
```

### EPUB Generation (requires Pandoc)

```bash
sudo apt install pandoc
pandoc _site/book.html -o assets/与廖耀湘有关的文字资料合集.epub --toc
```

### Plain Text Generation (Python only)

```bash
python3 -c "import re; html = open('_site/book.html').read(); clean = re.sub('<[^<]+?>', '', html); print('\n'.join(line.strip() for line in clean.splitlines() if line.strip()))" > assets/与廖耀湘有关的文字资料合集.txt
```

---

## Deprecated Methods

- **weasyprint**: Removed (use Puppeteer instead)
- **Manual commands**: Use `generate-book.sh` wrapper script
