import json, datetime, sys

hn_raw = """{"by":"stefanpie","descendants":352,"id":48055913,"score":574,"title":"Canvas is down as ShinyHunters threatens to leak schools' data","url":"https://www.theverge.com/tech/926458/canvas-shinyhunters-breach","time":1778192541}
{"by":"psxuaw","descendants":229,"id":48056227,"score":439,"title":"Maybe you shouldn't install new software for a bit","url":"https://xeiaso.net/blog/2026/abstain-from-install/","time":1778194931}
{"by":"PriorityLeft","descendants":394,"id":48054423,"score":634,"title":"Cloudflare to cut about 20% workforce","url":"https://www.reuters.com/business/world-at-work/cloudflare-cut-over-1100-jobs-2026-05-07/","time":1778185417}
{"by":"flipped","descendants":246,"id":48053623,"score":605,"title":"Dirtyfrag: Universal Linux LPE","url":"https://www.openwall.com/lists/oss-security/2026/05/07/8","time":1778181692}
{"by":"peter_d_sherman","descendants":7,"id":48058644,"score":36,"title":"Blaise \u2013 A modern self-hosting zero-legacy Object Pascal compiler targeting QBE","url":"https://github.com/graemeg/blaise","time":1778215442}
{"by":"speckx","descendants":311,"id":48049653,"score":629,"title":"The map that keeps Burning Man honest","url":"https://www.not-ship.com/burning-man-moop/","time":1778162770}
{"by":"cemsakarya","descendants":49,"id":48035420,"score":123,"title":"Pinocchio is weirder than you remembered","url":"https://storica.club/blog/pinocchio-in-italian/","time":1778070427}
{"by":"CliffStoll","descendants":10,"id":48037336,"score":73,"title":"Rumors of my death are slightly exaggerated","url":"https://www.facebook.com/story.php?story_fbid=989939243570691&id=100076638743004","time":1778081091}
{"by":"bsuh","descendants":216,"id":48051562,"score":446,"title":"Agents need control flow, not more prompts","url":"https://bsuh.bearblog.dev/agents-need-control-flow/","time":1778172215}
{"by":"lermontov","descendants":14,"id":48032393,"score":24,"title":"Inventing Cyrillic","url":"https://www.historytoday.com/archive/history-matters/inventing-cyrillic","time":1778043762}"""

github_trending = [
    ("Hmbown/DeepSeek-TUI", "Coding agent for DeepSeek models that runs in your terminal"),
    ("z-lab/dflash", "DFlash: Block Diffusion for Flash Speculative Decoding"),
    ("addyosmani/agent-skills", "Production-grade engineering skills for AI coding agents."),
    ("vercel-labs/open-agents", "An open source template for building cloud agents."),
]

items = []
for line in hn_raw.strip().split('\n'):
    d = json.loads(line)
    ts = datetime.datetime.fromtimestamp(d.get('time', 0))
    items.append({
        'title': d.get('title', ''),
        'url': d.get('url', ''),
        'score': d.get('score', 0),
        'by': d.get('by', ''),
        'descendants': d.get('descendants', 0),
        'time': ts.strftime('%Y-%m-%d %H:%M')
    })

today = datetime.date.today().strftime('%Y-%m-%d')
chinese_date = datetime.date.today().strftime('%Y年%m月%d日')

# Build HN table rows
hn_rows = []
for i, item in enumerate(items, 1):
    hn_rows.append(f"| {i} | [{item['title']}]({item['url']}) | {item['score']} | {item['by']} |")

# Build GitHub table rows
gh_rows = []
for repo, desc in github_trending:
    gh_rows.append(f"| [{repo}](https://github.com/{repo}) | {desc} |")

brief = f"""---
title: "晨报 {today}"
type: morning-brief
source: hacker-news, github-trending
date: {today}
created: {today}
tags: [news, daily, morning-brief]
---

# 📰 技术晨报 — {chinese_date}

> 自动生成 | 数据来源: Hacker News / GitHub Trending

## 🏆 Hacker News Top Stories

| # | 标题 | 分数 | 作者 |
|---|------|------|------|
{chr(10).join(hn_rows)}

## ⭐ GitHub Trending

| 项目 | 描述 |
|------|------|
{chr(10).join(gh_rows)}

## 📊 今日概要

- **热点话题：** Canvas 学习平台数据泄露事件（ShinyHunters 威胁公开学校数据）、Cloudflare 宣布裁员约 20%（1100+ 人）、Linux 本地提权漏洞 Dirtyfrag
- **值得关注的开源项目：** DeepSeek-TUI（终端 DeepSeek 交互）、agent-skills（AI 编程代理工程技能）、open-agents（云端 Agent 模板）
- **行业趋势：** AI Agent 控制流设计受关注、编译器领域有新玩家（Blaise Pascal 编译器）

## 🔗 延伸阅读

- [Canvas 数据泄露报道 (The Verge)](https://www.theverge.com/tech/926458/canvas-shinyhunters-breach)
- [Cloudflare 裁员新闻 (Reuters)](https://www.reuters.com/business/world-at-work/cloudflare-cut-over-1100-jobs-2026-05-07/)
- [Dirtyfrag 漏洞详情 (Openwall)](https://www.openwall.com/lists/oss-security/2026/05/07/8)
- [Agents need control flow (bsuh)](https://bsuh.bearblog.dev/agents-need-control-flow/)
- [DeepSeek-TUI (GitHub)](https://github.com/Hmbown/DeepSeek-TUI)
- [agent-skills (GitHub)](https://github.com/addyosmani/agent-skills)
"""

output_path = f"raw/morning-briefs/{today}.md"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(brief)

print(f"Written: {output_path}")
print(brief[:500])
