---
title: "Green Train Skills — README"
type: source
subtype: article
tags: [ai, ai-skill, tool]
created: 2026-05-05
updated: 2026-05-05
author: crazynomad（绿皮火车）
url: https://github.com/crazynomad/skills/blob/master/README.zh.md
date: 2026-05
sources:
  - "../../../raw/articles/greentrain-skills-readme.md"
---

# Green Train Skills — README

> 绿皮火车出品的 Claude Code Agent 技能合集，涵盖媒体处理、文件管理（macOS）和 PPT 方法论三大插件包，通过 `npx skills add` 一行安装。

## 核心论点

1. AI Skills 可以按功能域打包为插件（plugin），通过统一市场 `skills.sh` 分发；`npx skills add crazynomad/skills` 即可注册。
2. 文件管理三件套（disk-cleaner / file-organizer / doc-mindmap）形成「清→理→知」流水线，实测释放 120GB 空间、整理 1600+ 文件、将 4000+ PPT 转为可检索知识库。
3. doc-mindmap 和 tts 两个技能强调**本地 AI**（Ollama + Vox CLI），所有处理在设备端完成，数据不离机。
4. PPT 方法论三件套（ppt-classify / ppt-research-setup / ppt-narrative-review）形成「分类→立论→评审」前置工作流，核心主张：先想清楚结构再开 PowerPoint。
5. podcast-downloader 诞生于 Vibe Coding 挑战——Claude + Gemini + NotebookLM 三回合 AI 协作逆向工程 Apple 播客 API，体现 AI 辅助工具开发的典型范式。

## 关键摘录

> "通过简单的 AI 指令即可完成复杂操作。"

> "所有 AI 处理通过 Ollama 在本地运行，文档不会离开你的电脑。"（doc-mindmap）

> "所有处理完全在设备上运行，数据不会离开你的电脑。"（tts）

> "先想清楚再开 PowerPoint"（greentrain-planning 插件定位）

> "Specificity is the only currency. Vague answers get pushed."（ppt-research-setup）

**技能清单（14 个）**：
| 插件包 | 技能 |
|--------|------|
| greentrain-files | file-master, disk-cleaner, file-organizer, doc-mindmap |
| greentrain-media | pdf-to-images, podcast-downloader, srt-title-generator, tts, twitter-downloader, visual-deck, youtube-downloader |
| greentrain-planning | ppt-classify, ppt-research-setup, ppt-narrative-review |

## 提到的实体

- [[../../entities/products/greentrain-skills|greentrain-skills]] — 本项目本身

## 提到的概念

- [[../../concepts/ai/ai-skills|AI Skills 生态]] — 本资料是该生态的新成员案例
