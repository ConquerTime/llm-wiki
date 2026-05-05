---
title: "本地 AI 处理（Local AI Processing）"
type: concept
subtype: ai
tags: [ai, tool]
created: 2026-05-05
updated: 2026-05-05
sources:
  - "[[raw/articles/greentrain-skills-readme.md|Green Train Skills README]]"
---

# 本地 AI 处理（Local AI Processing）

> 将 AI 推理/生成负载跑在用户设备上，而非发送到云端服务器，数据不离机。

## 核心特征

- **数据隔离**：用户文档、音频、图像不经过第三方服务器
- **离线可用**：网络中断后仍可运行（推理本地化）
- **运行时依赖**：通常需要本地模型运行框架（Ollama、MLX 等）
- **硬件约束**：大模型需要足够 RAM/VRAM，Apple Silicon 是当前主流本地推理平台

## 典型工具栈

| 场景 | 工具 | 来源 |
|------|------|------|
| 文档摘要/分类 | [Ollama](https://ollama.com/) | doc-mindmap（greentrain-skills） |
| TTS/STT/声音克隆 | Vox CLI（Qwen3-TTS + MLX） | tts（greentrain-skills） |
| 通用本地推理 | Ollama、llama.cpp | 多个项目 |

## 与相关概念的关系

- **vs 云端 API（如 Claude API）**：云端延迟低、能力强，但数据出境；本地处理反之
- **vs [[mcp|MCP]]**：MCP 是工具协议层，本地 AI 处理是执行层——两者可组合
- **vs [[rag|RAG]]**：RAG 的检索和生成可以全部本地化，也可以混合

## 开放问题

- Apple Silicon 之外的平台（Windows/Linux GPU）生态成熟度如何？
- 本地模型能力增长是否会使云端方案的优势缩窄到只剩最新 frontier 模型？

## 来源

- [[../../raw/articles/greentrain-skills-readme.md|Green Train Skills README]]
