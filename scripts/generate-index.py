#!/usr/bin/env python3
"""
Wiki Index Generator — 自动生成内容索引

用法:
    python scripts/generate-index.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime

WIKI_ROOT = Path(__file__).parent.parent / "wiki"
INDEX_FILE = WIKI_ROOT / "index.md"


def get_all_pages() -> dict:
    """获取所有 wiki 页面的分类信息"""
    categories = {
        "entities/persons": [],
        "entities/organizations": [],
        "entities/products": [],
        "entities/locations": [],
        "concepts": [],
        "sources/articles": [],
        "sources/papers": [],
        "sources/books": [],
        "synthesis": [],
        "questions": [],
    }
    
    for md_file in WIKI_ROOT.rglob("*.md"):
        if md_file.name.startswith(".") or md_file.name in ["index.md", "log.md"]:
            continue
        
        rel_path = md_file.relative_to(WIKI_ROOT)
        category = str(rel_path.parent)
        
        # 读取 frontmatter
        content = md_file.read_text(encoding="utf-8")
        title = md_file.stem
        summary = ""
        sources_count = 0
        date = ""
        
        in_frontmatter = False
        frontmatter_lines = []
        body_lines = []
        in_body = False
        
        for line in content.split("\n"):
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    in_body = True
                    continue
            elif in_frontmatter:
                frontmatter_lines.append(line)
            elif in_body:
                body_lines.append(line)
        
        # 解析 frontmatter
        for line in frontmatter_lines:
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip()
            elif line.startswith("sources:"):
                import re
                sources_match = re.findall(r'\[([^\]]+)\]', line)
                if sources_match:
                    sources_count = len(sources_match[0].split(","))
            elif line.startswith("created:"):
                date = line.split(":", 1)[1].strip()
        
        # 生成摘要（取前 100 字符）
        body_text = " ".join(body_lines).strip()
        if len(body_text) > 100:
            summary = body_text[:100] + "..."
        else:
            summary = body_text
        
        entry = {
            "path": str(rel_path),
            "title": title,
            "summary": summary,
            "sources": sources_count,
            "date": date,
        }
        
        if category in categories:
            categories[category].append(entry)
        elif "entities" in category:
            categories["entities/persons"].append(entry)  # 默认放到 persons
        else:
            categories.setdefault(category, []).append(entry)
    
    return categories


def generate_index(categories: dict) -> str:
    """生成 index.md 内容"""
    lines = [
        "# 知识库索引",
        "",
        f"> 最后更新：{datetime.now().strftime('%Y-%m-%d')}",
        "",
        "本索引按类别组织所有 wiki 页面。",
        "",
    ]
    
    # 统计
    total = sum(len(pages) for pages in categories.values())
    lines.append(f"**总计：{total} 页面**\n")
    
    # 实体
    if categories.get("entities/persons") or categories.get("entities/organizations"):
        lines.append("## 实体 (Entities)")
        
        for subcat in ["entities/persons", "entities/organizations", "entities/products", "entities/locations"]:
            pages = categories.get(subcat, [])
            if pages:
                name = subcat.split("/")[-1].title()
                lines.append(f"\n### {name}")
                lines.append("")
                lines.append("| 页面 | 摘要 | 来源数 |")
                lines.append("|------|------|--------|")
                for page in sorted(pages, key=lambda x: x["title"]):
                    title_link = f"[{page['title']}]({page['path']})"
                    summary = page["summary"][:40] + "..." if len(page["summary"]) > 40 else page["summary"]
                    lines.append(f"| {title_link} | {summary} | {page['sources']} |")
    
    # 概念
    if categories.get("concepts"):
        lines.append("\n## 概念 (Concepts)")
        lines.append("")
        lines.append("| 页面 | 摘要 |")
        lines.append("|------|------|")
        for page in sorted(categories["concepts"], key=lambda x: x["title"]):
            title_link = f"[{page['title']}]({page['path']})"
            summary = page["summary"][:50] + "..." if len(page["summary"]) > 50 else page["summary"]
            lines.append(f"| {title_link} | {summary} |")
    
    # 源摘要
    for subcat, name in [
        ("sources/articles", "文章"),
        ("sources/papers", "论文"),
        ("sources/books", "书籍"),
    ]:
        pages = categories.get(subcat, [])
        if pages:
            lines.append(f"\n## 源摘要 - {name} ({name})")
            lines.append("")
            lines.append("| 页面 | 来源 | 日期 |")
            lines.append("|------|------|------|")
            for page in sorted(pages, key=lambda x: x["date"] if x["date"] else ""):
                title_link = f"[{page['title']}]({page['path']})"
                lines.append(f"| {title_link} | — | {page['date']} |")
    
    # 综合分析
    if categories.get("synthesis"):
        lines.append("\n## 综合分析 (Synthesis)")
        lines.append("")
        for page in sorted(categories["synthesis"], key=lambda x: x["date"] if x["date"] else ""):
            title_link = f"[{page['title']}]({page['path']})"
            lines.append(f"- {title_link}: {page['summary'][:60]}...")
    
    # 问答存档
    if categories.get("questions"):
        lines.append("\n## 问答存档 (Questions)")
        lines.append("")
        for page in sorted(categories["questions"], key=lambda x: x["date"] if x["date"] else ""):
            title_link = f"[{page['title']}]({page['path']})"
            lines.append(f"- {title_link}: {page['summary'][:60]}...")
    
    return "\n".join(lines)


def main():
    print("📊 正在生成索引...")
    
    categories = get_all_pages()
    index_content = generate_index(categories)
    
    INDEX_FILE.write_text(index_content, encoding="utf-8")
    
    total = sum(len(pages) for pages in categories.values())
    print(f"✅ 索引已更新：{INDEX_FILE}")
    print(f"   共 {total} 个页面")


if __name__ == "__main__":
    main()
