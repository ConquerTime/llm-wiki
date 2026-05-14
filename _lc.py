#!/usr/bin/env python3
import os, re
from collections import defaultdict

wiki = 'wiki'
wikilink_pattern = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')

path_keys = {}
title_to_path = {}
wiki_pages = {}

for root, dirs, files in os.walk(wiki):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['_archive']]
    for fname in files:
        if not fname.endswith('.md') or fname.startswith('_'):
            continue
        rel_path = os.path.relpath(os.path.join(root, fname), wiki)
        full_path = os.path.join(root, fname)
        wiki_pages[rel_path] = full_path
        key = rel_path[:-3] if rel_path.endswith('.md') else rel_path
        path_keys[key] = rel_path
        path_keys[key.lower()] = rel_path
        path_keys[key.lower().split('/')[-1]] = rel_path
        parts = key.split('/')
        for i in range(len(parts)):
            path_keys['/'.join(parts[i:]).lower()] = rel_path
        with open(full_path, encoding='utf-8') as f:
            content = f.read()
            m = re.search(r'^title:\s*["\']?([^"\'\n]+)["\']?', content, re.MULTILINE)
        if m:
            title = m.group(1).strip()
            title_to_path[title.lower()] = rel_path
            path_keys[title.lower()] = rel_path

def resolve_link(link_text, page_rel_path):
    lt = link_text.strip()
    if lt in path_keys: return path_keys[lt]
    if lt.lower() in path_keys: return path_keys[lt.lower()]
    if lt.lower() in title_to_path: return title_to_path[lt.lower()]
    if (lt + '.md') in path_keys: return path_keys[lt + '.md']
    if lt.startswith('../'):
        parts = lt.split('/')
        up_count = 0
        rest_parts = []
        for p in parts:
            if p == '..': up_count += 1
            else: rest_parts.append(p)
        page_dir = os.path.dirname(page_rel_path)
        page_components = page_dir.split('/')
        target = '/'.join(page_components[:-up_count] + rest_parts) if up_count <= len(page_components) else '/'.join(rest_parts)
        if target in path_keys: return path_keys[target]
        if target.lower() in path_keys: return path_keys[target.lower()]
        if (target + '.md') in path_keys: return path_keys[target + '.md']
    return None

inbound = defaultdict(set)
broken_links = []
for rel_path, full_path in wiki_pages.items():
    content = open(full_path, encoding='utf-8').read()
    for link in wikilink_pattern.findall(content):
        if link == 'page' or '../../raw/' in link or '../raw/' in link:
            continue
        if resolved := resolve_link(link, rel_path):
            inbound[resolved].add(rel_path)
        else:
            broken_links.append((rel_path, link))

expected_orphan = {'index.md', 'log.md'} | {p for p in wiki_pages if p.startswith('sources/')}
orphans = [p for p in wiki_pages if p not in expected_orphan and not inbound[p]]

print(f'Total wiki pages: {len(wiki_pages)}')
print(f'Orphans: {len(orphans)}')
print(f'Broken links: {len(broken_links)}')
