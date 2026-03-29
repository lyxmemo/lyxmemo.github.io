#!/usr/bin/env bash
# Usage:
#   ./commit-article.sh                    # reads content from clipboard (pbpaste)
#   ./commit-article.sh article.txt        # reads content from file
#
# Creates the article file directly and commits it (no GitHub issue).
set -euo pipefail
cd "$(dirname "$0")"

# ── Colors ──
bold='\033[1m' dim='\033[2m' reset='\033[0m' green='\033[32m' yellow='\033[33m' red='\033[31m'

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
ckey="${collections[$((cnum-1))]%% *}"
echo ""

# ── Battles subfolder (if needed) ──
subfolder=""
if [[ "$ckey" == "battles_history" ]]; then
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
[[ "$toc_input" =~ ^[Yy] ]] && toc=true || toc=false

read -rp "备注 / Notes (可选，回车跳过): " notes

# ── Determine destination path ──
case "$ckey" in
  newspapers)
    # Filename: YYYYMMDD + title (strip dashes from date)
    dateprefix="${date//-/}"
    filename="${dateprefix}${title}.md"
    destdir="docs/_newspapers"
    ;;
  battles_history)
    filename="${title}（${author}）.md"
    destdir="docs/_battles_history/${subfolder}"
    ;;
  liaos_writings)
    filename="${title}（${author}）.md"
    destdir="docs/_liaos_writings"
    ;;
  liaos_tele)
    filename="${title}.md"
    destdir="docs/_liaos_tele"
    ;;
  n6a_memorial)
    filename="${title}（${author}）.md"
    destdir="docs/_n6a_memorial"
    ;;
  n22d_memorial)
    filename="${title}（${author}）.md"
    destdir="docs/_n22d_memorial"
    ;;
  ten_year_memorial)
    filename="${title}（${author}）.md"
    destdir="docs/_ten_year_memorial"
    ;;
  *)
    echo -e "${red}未知文集: ${ckey}${reset}"
    exit 1
    ;;
esac

destpath="${destdir}/${filename}"

# ── Safety check ──
if [[ -f "$destpath" ]]; then
  echo -e "${red}文件已存在: ${destpath}${reset}"
  read -rp "覆盖? [y/N]: " overwrite
  [[ "$overwrite" =~ ^[Yy] ]] || exit 1
fi

# ── Ensure destination directory exists ──
mkdir -p "$destdir"

# ── Build front matter ──
frontmatter="---
layout: post
title: \"${title}\"
author: \"${author}\"
category: \"${category}\"
tags: 分类
date:  ${date} 00:00:00 +0000"

if $toc; then
  frontmatter="${frontmatter}
toc: true"
fi

frontmatter="${frontmatter}
---"

# ── Build file body based on collection type ──
body=""

case "$ckey" in
  newspapers)
    # Newspapers: source line at top and bottom
    if [[ -n "$source" ]]; then
      body="> ${source}

${content}

> ${source}"
    else
      body="$content"
    fi
    ;;
  *)
    # Articles: author line, transcriber, then content, then source
    body="> ${author}

录入校对：${transcriber}

${content}"
    if [[ -n "$source" ]]; then
      body="${body}

> 来源：${source}"
    fi
    ;;
esac

# ── Write file ──
{
  echo "$frontmatter"
  echo ""
  echo "$body"
} > "$destpath"

echo ""
echo -e "${green}${bold}✓ 文件已创建: ${destpath}${reset}"
echo -e "${dim}  共 $(wc -l < "$destpath" | tr -d ' ') 行${reset}"

# ── Show notes if any ──
if [[ -n "$notes" ]]; then
  echo -e "${yellow}备注: ${notes}${reset}"
fi

# ── Git commit ──
echo ""
read -rp "是否提交? / Commit now? [Y/n]: " do_commit
if [[ ! "$do_commit" =~ ^[Nn] ]]; then
  git add "$destpath"
  git commit -m "添加文章：${title}"
  echo -e "${green}${bold}✓ 已提交${reset}"

  read -rp "是否推送? / Push now? [y/N]: " do_push
  if [[ "$do_push" =~ ^[Yy] ]]; then
    branch="$(git branch --show-current)"
    git push -u origin "$branch"
    echo -e "${green}${bold}✓ 已推送到 ${branch}${reset}"
  fi
else
  echo -e "${dim}文件已创建但未提交，可手动 git add & commit${reset}"
fi
