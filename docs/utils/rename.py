import os
import re

# --- 配置区 ---
# 请将此路径修改为您存放 .md 文件的文件夹路径
# 使用 '.' 表示当前目录
TARGET_DIRECTORY = '../_liaos_writings/' 

# 新的 category 和 tags 值
NEW_CATEGORY = "廖耀湘文集"
NEW_TAGS = "分类"
# 默认作者（当标题中找不到作者时使用）
DEFAULT_AUTHOR = "廖耀湘"
# --- 配置区结束 ---

def process_markdown_file(file_path):
    """
    处理单个 Markdown 文件，更新其 Front Matter。
    """
    print(f"正在处理文件: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用正则表达式查找 Front Matter 分隔符 ---
        # re.DOTALL 让 '.' 可以匹配包括换行在内的任意字符
        match = re.match(r'---\s*(.*?)\s*---\s*(.*)', content, re.DOTALL)

        if not match:
            print(f"  -> 警告: 在 {file_path} 中未找到有效的 Front Matter 结构，已跳过。")
            return

        front_matter_str = match.group(1)
        body_content = match.group(2)

        # 1. 提取原始标题
        title_match = re.search(r'title:\s*["\'](.*?)["\']', front_matter_str)
        if not title_match:
            print(f"  -> 警告: 在 {file_path} 的 Front Matter 中未找到 'title'，已跳过。")
            return
        original_title = title_match.group(1)

        # 2. 从原始标题中提取作者
        author_match = re.search(r'（([^）]+)）', original_title)
        if author_match:
            author = author_match.group(1).strip()
            # 从标题中移除作者和括号
            new_title = re.sub(r'（[^）]+）', '', original_title).strip()
        else:
            author = DEFAULT_AUTHOR
            new_title = original_title # 如果没有作者，标题保持不变
            print(f"  -> 信息: 在标题 '{original_title}' 中未找到作者，使用默认作者 '{DEFAULT_AUTHOR}'。")

        # 3. 构建新的 Front Matter
        new_front_matter = f"""---
layout: post
title: "{new_title}"
author: "{author}"
category: "{NEW_CATEGORY}"
tags: {NEW_TAGS}
date:  1900-01-01 00:00:00 +0000
---"""

        # 4. 组合新的内容并写回文件
        new_content = new_front_matter + "\n" + body_content.lstrip()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  -> 成功: 文件已更新。标题: '{new_title}', 作者: '{author}'")

    except Exception as e:
        print(f"  -> 错误: 处理文件 {file_path} 时发生错误: {e}")


def main():
    """
    脚本主函数，遍历目录并处理文件。
    """
    if not os.path.isdir(TARGET_DIRECTORY):
        print(f"错误: 目录 '{TARGET_DIRECTORY}' 不存在。请检查路径配置。")
        return

    print(f"开始扫描目录: {TARGET_DIRECTORY}")
    # 遍历目录及子目录下的所有文件
    for root, _, files in os.walk(TARGET_DIRECTORY):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                process_markdown_file(file_path)
    
    print("\n所有 .md 文件处理完毕。")


if __name__ == '__main__':
    main()
