#!/usr/bin/env python3
"""
Wiki Search Tool — 本地 Markdown 文件搜索
支持模糊匹配和正则表达式

用法:
    python scripts/search.py <关键词>
    python scripts/search.py <关键词> --regex
    python scripts/search.py <关键词> --files  # 只返回文件名
"""

import os
import re
import sys
import argparse
from pathlib import Path

WIKI_ROOT = Path(__file__).parent.parent / "wiki"
RAW_ROOT = Path(__file__).parent.parent / "raw"


def search_keyword(keyword: str, regex: bool = False, files_only: bool = False) -> list:
    """搜索 wiki 和 raw 目录中的 Markdown 文件"""
    results = []
    
    for root in [WIKI_ROOT, RAW_ROOT]:
        if not root.exists():
            continue
            
        for md_file in root.rglob("*.md"):
            # 跳过隐藏文件和 index/log
            if md_file.name.startswith(".") or md_file.name in ["index.md", "log.md"]:
                continue
                
            try:
                content = md_file.read_text(encoding="utf-8")
                lines = content.split("\n")
                
                if regex:
                    pattern = re.compile(keyword, re.IGNORECASE)
                    matches = []
                    for i, line in enumerate(lines, 1):
                        if pattern.search(line):
                            matches.append((i, line.strip()))
                else:
                    keyword_lower = keyword.lower()
                    matches = []
                    for i, line in enumerate(lines, 1):
                        if keyword_lower in line.lower():
                            matches.append((i, line.strip()))
                
                if matches:
                    rel_path = md_file.relative_to(root.parent)
                    results.append({
                        "file": str(rel_path),
                        "matches": matches,
                        "match_count": len(matches)
                    })
                    
            except Exception as e:
                print(f"Warning: Error reading {md_file}: {e}", file=sys.stderr)
    
    return results


def print_results(results: list, files_only: bool = False):
    """格式化输出搜索结果"""
    if not results:
        print("未找到匹配结果。")
        return
    
    total_matches = sum(r["match_count"] for r in results)
    print(f"\n找到 {len(results)} 个文件，{total_matches} 处匹配：\n")
    
    for result in results:
        print(f"📄 {result['file']}")
        
        if not files_only:
            for line_num, line_content in result["matches"][:5]:  # 最多显示5处
                print(f"   {line_num}: {line_content[:100]}")
            
            if len(result["matches"]) > 5:
                print(f"   ... 还有 {len(result['matches']) - 5} 处匹配")
        print()


def main():
    parser = argparse.ArgumentParser(description="Wiki 搜索工具")
    parser.add_argument("keyword", help="搜索关键词")
    parser.add_argument("--regex", "-r", action="store_true", help="使用正则表达式")
    parser.add_argument("--files", "-f", action="store_true", help="只显示文件名")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有 wiki 页面")
    
    args = parser.parse_args()
    
    if args.list:
        # 列出所有页面
        print("\n📚 Wiki 页面列表：\n")
        for md_file in sorted(WIKI_ROOT.rglob("*.md")):
            if md_file.name.startswith("."):
                continue
            rel = md_file.relative_to(WIKI_ROOT.parent)
            print(f"  {rel}")
        print()
        return
    
    results = search_keyword(args.keyword, regex=args.regex, files_only=args.files)
    print_results(results, files_only=args.files)


if __name__ == "__main__":
    main()
