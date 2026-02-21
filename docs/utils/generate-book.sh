#!/bin/bash

# PDF Generation Script
# Generates PDF/EPUB/TXT from Jekyll-built HTML

set -e

# Get script directory and navigate to docs root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$(dirname "$SCRIPT_DIR")"
cd "$DOCS_DIR"

INPUT_HTML="${1:-./_site/book.html}"
OUTPUT_DIR="${2:-.}/assets"
FILENAME="${3:-与廖耀湘有关的文字资料合集}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📚 Book Generator${NC}"
echo "Input: $INPUT_HTML"
echo "Output Directory: $OUTPUT_DIR"
echo ""

# Check if input file exists
if [ ! -f "$INPUT_HTML" ]; then
  echo "Error: Input file not found: $INPUT_HTML"
  echo "Did you run 'bundle exec jekyll serve' first?"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# 1. Generate PDF using Node.js + Puppeteer
echo -e "${BLUE}[1] Generating PDF...${NC}"
if ! npx puppeteer --version &> /dev/null; then
  echo "Installing puppeteer..."
  npm install puppeteer --legacy-peer-deps
fi

node "$(dirname "$0")/generate_pdf.js" "$INPUT_HTML" "$OUTPUT_DIR/$FILENAME.pdf"
echo -e "${GREEN}✓ PDF generated${NC}"

# 2. Generate EPUB using Pandoc
echo ""
echo -e "${BLUE}[2] Generating EPUB...${NC}"
if command -v pandoc &> /dev/null; then
  pandoc "$INPUT_HTML" -o "$OUTPUT_DIR/$FILENAME.epub" --toc
  echo -e "${GREEN}✓ EPUB generated${NC}"
else
  echo "⚠ Pandoc not found, skipping EPUB generation"
  echo "  Install with: sudo apt install pandoc"
fi

# 3. Generate plain text
echo ""
echo -e "${BLUE}[3] Generating plain text...${NC}"
python3 -c "import re; html = open('$INPUT_HTML').read(); clean = re.sub('<[^<]+?>', '', html); print('\n'.join(line.strip() for line in clean.splitlines() if line.strip()))" > "$OUTPUT_DIR/$FILENAME.txt"
echo -e "${GREEN}✓ Plain text generated${NC}"

echo ""
echo -e "${GREEN}✅ All conversions complete!${NC}"
echo "Output files in: $OUTPUT_DIR/"
