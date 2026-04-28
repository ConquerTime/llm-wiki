---
title: LLM Wiki
type: concept
subtype: ai
tags: [pkm, llm, knowledge-base]
created: 2026-04-14
updated: 2026-04-15
sources:
  - ../../raw/articles/llm-wiki-by-karpathy.md
---

# LLM Wiki

> 由 LLM 增量构建和维护的持久个人知识库模式，知识编译一次后持续保持最新。

## 是什么

一种用 LLM 管理个人知识的模式。核心思路：不让 LLM 在每次提问时临时检索文档（RAG 模式），而是让它**持续构建一个结构化的 wiki**。每次摄入新资料，LLM 会读取、提取、整合到已有的知识网络中——更新实体页、修改概念页、标注矛盾、维护交叉引用。

与 [[rag|RAG]] 的本质区别：RAG 是"每次重新推导"，LLM Wiki 是"编译一次，持续维护"。

## 三层架构

```
Raw Sources (不可变)  →  Wiki (LLM 维护)  →  Schema (CLAUDE.md)
```

1. **Raw Sources** — 原始资料，只读。LLM 绝不修改。
2. **Wiki** — LLM 生成并维护的 markdown 文件集合。包含源摘要、概念页、实体页、综合分析。
3. **Schema** — 给 LLM 的指令手册，定义结构、格式、工作流。

## 三种操作

- **Ingest** — 摄入新资料，触发 wiki 的增量更新
- **Query** — 基于 wiki 回答问题，优质回答可存档为新页面
- **Lint** — 健康检查：矛盾检测、过时信息、孤立页面、缺失链接

## 为什么有效

人类放弃 wiki 的原因是维护负担增长快于价值。LLM 消除了这个瓶颈：它不会厌倦、不会忘记更新交叉引用、一次可以修改多个文件。人类只需要做高价值的事：策展来源、引导分析、提出好问题。

## 开放问题

- 规模上限在哪？index.md 在 ~100 个源、~数百页面时够用，之后需要搜索引擎
- 多 LLM 协作维护同一个 wiki 是否可行？
- 如何处理 LLM 的幻觉风险？wiki 中的错误会被后续操作放大

## 来源

- 首次提出：[[sources/articles/llm-wiki-by-karpathy|Karpathy 2026]]

## 相关概念

- [[ai-skills|AI Skills 生态]] — Skills 是 LLM Wiki 能力封装化的延伸趋势
