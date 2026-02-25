#!/usr/bin/env bash
# Usage:
#   ./add-article.sh                    # reads content from clipboard (pbpaste)
#   ./add-article.sh article.txt        # reads content from file
set -euo pipefail
cd "$(dirname "$0")"

# ── Colors ──
bold='\033[1m' dim='\033[2m' reset='\033[0m' green='\033[32m' yellow='\033[33m'

# ── Read content first ──
if [[ -n "${1:-}" && -f "${1:-}" ]]; then
  content="$(cat "$1")"
  echo -e "${dim}从文件读取: $1${reset}"
else
  echo -e "${bold}请先将文章内容复制到剪贴板，然后按回车继续...${reset}"
  read -r
  content="$(pbpaste)"
fi

# Show preview
line_count=$(echo "$content" | wc -l | tr -d ' ')
char_count=$(echo -n "$content" | wc -c | tr -d ' ')
echo -e "${dim}── 内容预览 (${line_count} 行, ${char_count} 字) ──${reset}"
echo "$content" | head -3
echo -e "${dim}...${reset}"
echo "$content" | tail -2
echo -e "${dim}── 预览结束 ──${reset}"
echo ""

# ── Collection picker ──
echo -e "${bold}选择文集 / Pick a collection:${reset}"
collections=(
  "liaos_writings (廖耀湘文集)"
  "liaos_tele (来往电报)"
  "newspapers (报刊杂志)"
  "n6a_memorial (新六军纪念)"
  "n22d_memorial (新二十二师纪念)"
  "ten_year_memorial (故人回忆)"
  "battles_history (战史)"
)
for i in "${!collections[@]}"; do
  echo "  $((i+1)). ${collections[$i]}"
done
read -rp "输入编号 [1-7]: " cnum
collection="${collections[$((cnum-1))]}"
echo ""

# ── Battles subfolder (if needed) ──
subfolder="N/A"
if [[ "$collection" == battles_history* ]]; then
  echo -e "${bold}选择子目录 / Pick subfolder:${reset}"
  subfolders=("1939" "1942" "1943" "1944" "1945" "liaoshen/1946" "liaoshen/1947" "liaoshen/1948")
  for i in "${!subfolders[@]}"; do
    echo "  $((i+1)). ${subfolders[$i]}"
  done
  read -rp "输入编号 [1-8]: " snum
  subfolder="${subfolders[$((snum-1))]}"
  echo ""
fi

# ── Metadata ──
read -rp "标题 / Title: " title
read -rp "作者 / Author: " author

# Auto-set category for fixed collections, otherwise ask
ckey="${collection%% *}"
case "$ckey" in
  liaos_writings) category="廖耀湘文集" ;;
  liaos_tele)     category="Liao's Tele" ;;
  newspapers)     category="报刊杂志" ;;
  *)
    read -rp "分类 / Category: " category
    ;;
esac

read -rp "日期 / Date [1900-01-01]: " date
date="${date:-1900-01-01}"

read -rp "来源 / Source (可选，回车跳过): " source
read -rp "录入校对 / Transcriber [观棋不语]: " transcriber
transcriber="${transcriber:-观棋不语}"

echo -e "${dim}添加目录？长文章含多个章节标题时选 Yes${reset}"
read -rp "TOC? [y/N]: " toc_input
[[ "$toc_input" =~ ^[Yy] ]] && toc="Yes" || toc="No"

read -rp "备注 / Notes (可选，回车跳过): " notes

# ── Write body to temp file to avoid argument length limits ──
tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT

cat > "$tmpfile" <<ENDOFBODY
### Collection / 文集

${collection}

### Battles subfolder / 战史子目录

${subfolder}

### Title / 标题

${title}

### Author / 作者

${author}

### Category / 分类

${category}

### Date / 日期

${date}

### Source / 来源

${source}

### Transcriber / 录入校对

${transcriber}

### Add TOC / 添加目录

${toc}

### Content / 文章内容

${content}

### Notes / 备注

${notes}
ENDOFBODY

# ── Create issue ──
echo ""
echo -e "${bold}正在创建 Issue...${reset}"

url=$(gh issue create \
  --repo lyxmemo/lyxmemo.github.io \
  --title "[新文章] ${title}" \
  --label "new-article" \
  --body-file "$tmpfile")

echo -e "${green}${bold}✓ Issue 已创建: ${url}${reset}"
echo -e "${dim}PR 将在约 1 分钟后自动生成。${reset}"
