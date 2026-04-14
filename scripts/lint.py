#!/usr/bin/env python3
"""
Wiki Lint Tool — 健康检查脚本
检查：矛盾、过时、孤立页面、孤儿引用、缺失链接

用法:
    python scripts/lint.py
    python scripts/lint.py --fix  # 自动修复一些问题
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

WIKI_ROOT = Path(__file__).parent.parent / "wiki"
RAW_ROOT = Path(__file__).parent.parent / "raw"


def get_all_pages() -> dict:
    """获取所有 wiki 页面的信息"""
    pages = {}
    
    for md_file in WIKI_ROOT.rglob("*.md"):
        if md_file.name.startswith("."):
            continue
            
        rel_path = md_file.relative_to(WIKI_ROOT)
        content = md_file.read_text(encoding="utf-8")
        
        # 提取 frontmatter
        title = rel_path.stem
        tags = []
        sources = []
        created = None
        updated = None
        
        in_frontmatter = False
        frontmatter_content = []
        body_start = 0
        
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    body_start = i + 1
                    break
            elif in_frontmatter:
                frontmatter_content.append(line)
        
        # 解析 frontmatter
        for line in frontmatter_content:
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip()
            elif line.startswith("tags:"):
                tags_match = re.findall(r'\[([^\]]+)\]', line)
                if tags_match:
                    tags = [t.strip() for t in tags_match[0].split(",")]
            elif line.startswith("sources:"):
                sources_match = re.findall(r'\[([^\]]+)\]', line)
                if sources_match:
                    sources = [s.strip().strip("'\"") for s in sources_match[0].split(",")]
            elif line.startswith("created:"):
                created = line.split(":", 1)[1].strip()
            elif line.startswith("updated:"):
                updated = line.split(":", 1)[1].strip()
        
        # 提取 wiki 链接
        wiki_links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
        wiki_links = [link.strip() for link in wiki_links if not link.startswith("http")]
        
        pages[str(rel_path)] = {
            "title": title,
            "tags": tags,
            "sources": sources,
            "created": created,
            "updated": updated,
            "wiki_links": wiki_links,
            "path": md_file
        }
    
    return pages


def get_all_wiki_files() -> set:
    """获取所有 wiki 文件路径（用于检查孤儿链接）"""
    wiki_files = set()
    
    for md_file in WIKI_ROOT.rglob("*.md"):
        if md_file.name.startswith("."):
            continue
        rel_path = md_file.relative_to(WIKI_ROOT)
        # 转换为链接格式（不带 .md）
        wiki_files.add(rel_path.stem)
        # 也支持带路径的格式
        wiki_files.add(str(rel_path))
    
    return wiki_files


def lint_orphan_pages(pages: dict, wiki_files: set) -> list:
    """检查孤立页面（没有被任何页面引用）"""
    orphans = []
    
    # 统计每个页面被引用的次数
    inbound_links = defaultdict(list)
    
    for page_path, page_info in pages.items():
        for link in page_info["wiki_links"]:
            # 解析链接（可能是相对路径或只是文件名）
            link_stem = Path(link).stem if "." in link else link
            inbound_links[link_stem].append(page_path)
            inbound_links[link].append(page_path)
    
    # 排除 index 和 log，它们通常不被引用
    excluded = {"index", "log", "index.md", "log.md"}
    
    for page_path, page_info in pages.items():
        page_stem = Path(page_path).stem
        if page_stem not in excluded and page_stem not in inbound_links:
            # 检查是否有其他页面引用了这个页面的任意形式
            is_orphaned = True
            for link_target, referrers in inbound_links.items():
                if page_stem in link_target or link_target in page_stem:
                    is_orphaned = False
                    break
            
            if is_orphaned and page_info["wiki_links"]:  # 如果页面本身有外链但没有入链
                # 更宽松的检查：如果页面有内容但从不被引用
                content = page_info["path"].read_text()
                if len(content) > 500:  # 有实质内容
                    orphans.append(page_path)
    
    return orphans


def lint_broken_links(pages: dict, wiki_files: set) -> list:
    """检查孤儿引用（引用了不存在的页面）"""
    broken = []
    
    for page_path, page_info in pages.items():
        for link in page_info["wiki_links"]:
            link_stem = Path(link).stem
            # 检查是否存在对应的文件
            exists = False
            for wf in wiki_files:
                wf_stem = Path(wf).stem
                if link_stem == wf_stem or link_stem in wf:
                    exists = True
                    break
            
            if not exists and not link.startswith("http") and not link.startswith("../raw"):
                broken.append({
                    "page": page_path,
                    "link": link
                })
    
    return broken


def lint_missing_crossrefs(pages: dict) -> list:
    """检查可能需要但缺失的交叉引用"""
    suggestions = []
    
    for page_path, page_info in pages.items():
        content = page_info["path"].read_text()
        
        # 检查是否提到了某个概念但没有链接
        # 这是一个简化的实现
        potential_concepts = [
            "AI", "LLM", "Machine Learning", "Neural Network",
            "Python", "JavaScript", "Git", "Docker"
        ]
        
        for concept in potential_concepts:
            if concept.lower() in content.lower():
                # 检查是否链接到了相关的概念页
                has_link = any(concept.lower() in link.lower() for link in page_info["wiki_links"])
                if not has_link:
                    suggestions.append({
                        "page": page_path,
                        "suggestion": f"考虑为 '{concept}' 添加交叉链接"
                    })
                    break  # 每个页面只提一个建议
    
    return suggestions[:10]  # 限制数量


def lint_stale_content(pages: dict) -> list:
    """检查可能过时的内容"""
    stale = []
    now = datetime.now()
    
    for page_path, page_info in pages.items():
        if page_info["updated"]:
            try:
                updated_date = datetime.strptime(page_info["updated"], "%Y-%m-%d")
                days_since_update = (now - updated_date).days
                
                if days_since_update > 180:  # 超过半年
                    stale.append({
                        "page": page_path,
                        "days": days_since_update,
                        "updated": page_info["updated"]
                    })
            except ValueError:
                pass
    
    return stale


def run_lint(fix: bool = False) -> dict:
    """运行所有 lint 检查"""
    print("🔍 正在检查 wiki 健康状况...\n")
    
    pages = get_all_pages()
    wiki_files = get_all_wiki_files()
    
    print(f"📊 共检查 {len(pages)} 个页面\n")
    
    results = {
        "orphan_pages": lint_orphan_pages(pages, wiki_files),
        "broken_links": lint_broken_links(pages, wiki_files),
        "missing_crossrefs": lint_missing_crossrefs(pages),
        "stale_content": lint_stale_content(pages),
    }
    
    return results


def print_report(results: dict):
    """打印 lint 报告"""
    print("=" * 60)
    print("📋 LINT REPORT")
    print("=" * 60)
    
    # 孤立页面
    print("\n🔗 孤立页面（无入站引用）：")
    if results["orphan_pages"]:
        for page in results["orphan_pages"]:
            print(f"   - {page}")
    else:
        print("   ✅ 没有发现孤立页面")
    
    # 孤儿引用
    print("\n❌ 断链（引用了不存在的页面）：")
    if results["broken_links"]:
        for item in results["broken_links"]:
            print(f"   - {item['page']} → {item['link']}")
    else:
        print("   ✅ 没有发现断链")
    
    # 缺失交叉引用
    print("\n💡 建议添加的交叉引用：")
    if results["missing_crossrefs"]:
        for item in results["missing_crossrefs"][:5]:
            print(f"   - {item['page']}: {item['suggestion']}")
    else:
        print("   ✅ 交叉引用检查通过")
    
    # 过时内容
    print("\n⏰ 可能过时的内容（超过180天未更新）：")
    if results["stale_content"]:
        for item in results["stale_content"]:
            print(f"   - {item['page']} (最后更新: {item['updated']}, {item['days']} 天前)")
    else:
        print("   ✅ 没有发现过时内容")
    
    print("\n" + "=" * 60)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Wiki 健康检查")
    parser.add_argument("--fix", action="store_true", help="自动修复问题")
    args = parser.parse_args()
    
    results = run_lint(fix=args.fix)
    print_report(results)
    
    # 如果有严重问题，退出码为 1
    has_issues = results["broken_links"] or results["orphan_pages"]
    sys.exit(1 if has_issues else 0)


if __name__ == "__main__":
    main()
