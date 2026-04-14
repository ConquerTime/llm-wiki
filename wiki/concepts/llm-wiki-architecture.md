# LLM Wiki 架构

---
title: LLM Wiki 架构
tags: [llm, knowledge-base, architecture]
category: concepts
created: 2026-04-14
updated: 2026-04-14
sources: []
---

# LLM Wiki 架构

LLM Wiki 是一种由 LLM 增量构建和维护的个人知识库模式。

## 核心思想

传统 RAG 的问题：每次问答都是从零检索，LLM 不会"积累"知识。

LLM Wiki 的解决方案：让 LLM 在用户和原始资料之间构建一个**持久的、不断积累的 wiki**。

## 三层架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Raw Sources │ ──▶ │    Wiki    │ ──▶ │   Schema    │
│  (不可变)   │     │ (LLM 维护)  │     │ (CLAUDE.md) │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 1. Raw Sources（原始资料层）

- 存放所有原始文档：文章、论文、书籍
- **不可修改** — LLM 只读取，不改动
- 这是知识的唯一真实来源

### 2. Wiki（知识库层）

LLM 生成的摘要、实体、概念页面：

- **Entities** — 人物、组织、产品、地点
- **Concepts** — 术语、理论、方法
- **Sources** — 每个源文档的摘要
- **Synthesis** — 跨资料的综合分析
- **Questions** — 优秀问答存档

### 3. Schema（模式层）

给 LLM 的指令手册，定义：

- 目录结构规范
- 页面格式（frontmatter）
- Ingest/Query/Lint 工作流
- 命名规范
- Git 工作流

## 核心操作

### Ingest（摄入）

1. 添加新资料到 `raw/`
2. LLM 读取并分析
3. 创建/更新相关 wiki 页面
4. 更新 index.md 和 log.md

### Query（查询）

1. 用户提问
2. LLM 搜索 wiki 相关页面
3. 综合回答，标注来源
4. 优质回答可存档

### Lint（健康检查）

- 检查页面间矛盾
- 检测过时信息
- 发现孤立页面
- 补充缺失链接

## 优势

> "人类放弃 wiki 是因为维护负担增长快于价值。LLM 不会厌倦、不会忘记更新交叉引用、一次可以修改 15 个文件。"

- **积累性** — 知识一次编译，持续保持最新
- **交叉引用** — 页面间链接已建立，无需重复检索
- **维护自动化** — LLM 承担所有繁琐工作

## 工具链

- **Git** — 版本控制、分支管理
- **qmd** — 本地搜索（BM25 + 向量）
- **mdv** — 终端 Markdown 渲染
- **bat** — 语法高亮阅读

## 相关概念

- [[memex]] — Vannevar Bush 的 memex 设想
- [[personal-knowledge-management]] — 个人知识管理
- [[rag]] — 检索增强生成（对比）
