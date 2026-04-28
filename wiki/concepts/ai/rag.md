---
title: RAG (Retrieval-Augmented Generation)
type: concept
subtype: ai
tags: [ai, rag, llm]
created: 2026-04-15
updated: 2026-04-15
sources:
  - ../../raw/articles/llm-wiki-by-karpathy.md
---

# RAG

> 检索增强生成：LLM 在回答时从文档集合中检索相关片段作为上下文。

## 是什么

RAG 是当前最常见的 LLM + 文档使用模式。用户上传文件集合，系统建立索引（通常是向量嵌入），查询时检索相关片段，拼接到 LLM 的 prompt 中生成回答。NotebookLM、ChatGPT 文件上传等产品都属于此模式。

## 局限性

Karpathy 指出 RAG 的核心问题：**没有积累**。每次查询都是从头检索和推导，LLM 不会在多次交互间建立起对文档集合的整体理解。需要综合五篇文档才能回答的问题，每次都要重新拼凑。

## 与 LLM Wiki 的对比

| 方面 | RAG | [[llm-wiki|LLM Wiki]] |
|------|-----|----------|
| 知识积累 | 无，每次重新检索 | 有，持续整合 |
| 交叉引用 | 查询时临时建立 | 预先建立并维护 |
| 综合能力 | 受限于单次检索窗口 | 基于已编译的知识网络 |

## 来源

- [[sources/articles/llm-wiki-by-karpathy|Karpathy 2026]] — 作为 LLM Wiki 的对比对象被讨论
