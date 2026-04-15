---
title: "LLM Wiki — Karpathy"
type: source
subtype: article
tags: [llm, knowledge-base, wiki, rag]
author: Andrej Karpathy
url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
date: 2026-04
created: 2026-04-14
updated: 2026-04-15
sources:
  - ../../raw/articles/llm-wiki-by-karpathy.md
---

# LLM Wiki — Karpathy

> Karpathy 提出用 LLM 增量构建持久 wiki 来替代 RAG 的每次重检索。

## 核心论点

大多数人用 LLM 处理文档的方式是 RAG：上传文件、检索片段、生成回答。每次都从零推导，没有积累。Karpathy 提出了不同的模式：让 LLM 在用户和原始资料之间**增量构建一个持久的 wiki**。新资料不是被索引后等待检索，而是被读取、提取、整合进已有的知识结构。知识编译一次，持续保持最新。

## 关键摘录

> "the wiki is a persistent, compounding artifact. The cross-references are already there. The contradictions have already been flagged."

> "You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions."

> "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

> "Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass."

> "The idea is related in spirit to Vannevar Bush's Memex (1945) — a personal, curated knowledge store with associative trails between documents."

## 架构要素

- **三层**：Raw Sources（不可变）→ Wiki（LLM 维护）→ Schema（指令文档）
- **三操作**：Ingest（摄入新资料）→ Query（查询问答）→ Lint（健康检查）
- **两文件**：index.md（内容索引）+ log.md（时间线日志）

## 适用场景（原文列举）

- 个人成长追踪（目标、健康、心理）
- 研究深潜（数周数月的主题研究）
- 读书伴侣（角色、主题、情节线的 wiki）
- 团队知识库（Slack、会议、客户通话的整合）
- 竞品分析、尽调、旅行规划、课程笔记

## 工具推荐（原文提及）

- [[obsidian|Obsidian]] — 双向链接、图谱视图、Web Clipper
- **qmd** — 本地 Markdown 搜索（BM25 + 向量 + LLM 重排）
- **Marp** — Markdown 幻灯片
- **Dataview** — Obsidian frontmatter 查询插件

## 提到的实体

- [[andrej-karpathy|Andrej Karpathy]] — 作者
- [[obsidian|Obsidian]] — 推荐的人类界面

## 提到的概念

- [[llm-wiki|LLM Wiki]] — 本文核心概念
- [[rag|RAG]] — 对比对象
