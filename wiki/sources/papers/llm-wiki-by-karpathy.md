# LLM Wiki — Andrej Karpathy

---
title: "LLM Wiki — A Pattern for Building Personal Knowledge Bases"
tags: [llm, knowledge-base, karpathy, ai]
category: sources/papers
created: 2026-04-14
updated: 2026-04-14
sources: [https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f]
---

# LLM Wiki — Andrej Karpathy

> 来源：Andrej Karpathy 的 GitHub Gist，2026

## 核心摘要

Karpathy 提出了一种用 LLM 构建个人知识库的新模式：**LLM Wiki**。与传统的 RAG（检索增强生成）不同，LLM Wiki 不是在每次查询时重新检索文档，而是让 LLM **增量构建和维护一个持久的 wiki**。当添加新资料时，LLM 会读取、提取关键信息，并将新知识整合到现有 wiki 中——更新实体页面、修改主题摘要、标注矛盾之处、强化或挑战已有的综合认知。

## 关键要点

1. **持久积累** — 知识被编译一次，然后保持最新，不需要每次查询都重新推导
2. **LLM 是维护者** — 人类负责策展来源、提问、思考；LLM 负责总结、交叉引用、归档等所有繁琐工作
3. **三层架构** — Raw Sources（不可变）→ Wiki（LLM 维护）→ Schema（CLAUDE.md 指令）
4. **三种操作** — Ingest（摄入）、Query（查询）、Lint（健康检查）
5. **两个关键文件** — index.md（内容索引）、log.md（时间线日志）

## 与传统 RAG 的区别

| 方面 | 传统 RAG | LLM Wiki |
|------|----------|----------|
| 知识积累 | 无，每次重新检索 | 有，持续整合 |
| 交叉引用 | 需要时临时建立 | 预先建立并维护 |
| 维护成本 | 低（仅索引） | 接近零（LLM 自动化） |
| 回答质量 | 依赖检索质量 | 基于已编译的知识 |

## 适用场景

- **个人成长** — 追踪目标、健康、心理、自我提升
- **研究** — 深入研究某个主题数周或数月
- **读书** — 每读一章构建维基百科式的伴随笔记
- **团队知识库** — 由 LLM 维护的内部 wiki

## Karpathy 的工作流

> "实践中，我将 LLM Agent 放在一侧，Obsidian 放在另一侧。LLM 根据我们的对话进行编辑，我实时浏览结果——跟随链接、查看图谱、阅读更新的页面。Obsidian 是 IDE；LLM 是程序员；wiki 是代码库。"

## 架构图

```
Raw Sources          Wiki                  Schema
─────────────────────────────────────────────────
articles/       →   entities/         →   CLAUDE.md
papers/              concepts/
books/               sources/
                      synthesis/
                      questions/
                      index.md  ← 内容索引
                      log.md    ← 时间线日志
```

## 工具推荐

- **Obsidian** — 双向链接、图谱视图
- **Obsidian Web Clipper** — 浏览器剪藏
- **qmd** — 本地搜索（BM25 + 向量 + LLM 重排）
- **Marp** — Markdown 幻灯片
- **Dataview** — frontmatter 查询

## 为什么有效

> "人类放弃 wiki 是因为维护负担增长快于价值。LLM 不会厌倦、不会忘记更新交叉引用、一次可以修改 15 个文件。"
> — 维护成本接近零

## 相关页面

- [[llm-wiki-architecture]] — LLM Wiki 架构详解
