---
title: "Building Effective AI Agents"
type: source
author: Anthropic (Erik S. & Barry Zhang)
url: "https://www.anthropic.com/engineering/building-effective-agents"
date: 2026-05-08
created: 2026-05-10
updated: 2026-05-10
tags: [ai, agent, engineering]
sources:
  - ../../../raw/articles/anthropic/Building Effective AI Agents.md
---

# Building Effective AI Agents

> Anthropic 分享构建可靠 AI Agents 的实践经验：Workflows vs Agents 区分、五种基础模式、核心三原则。

## 核心论点

Anthropic 与数十个团队合作构建 LLM Agents，总结出最成功的实现不是使用复杂框架，而是简单的可组合模式：

### Workflows vs Agents 区分

- **Workflows**：通过预定义代码路径编排 LLM 和工具
- **Agents**：LLM 动态引导自己的流程和工具使用，保持控制

### 何时使用 Agents

- 建议先尝试最简单的方案（优化单个 LLM 调用 + retrieval + in-context examples）
- 只有在需要灵活性和模型驱动决策时才使用 Agents
- Agents 换取延迟和成本来获得更好的任务性能

### 五种基础模式

1. **Prompt Chaining**：任务分解为序列步骤，每个 LLM 处理前一个输出
2. **Routing**：分类输入并导向专门的后续任务
3. **Parallelization**：LLM 并行处理任务（Sectioning 或 Voting）
4. **Orchestrator-Workers**：中央 LLM 动态分解任务并委托给 Worker LLM
5. **Evaluator-Optimizer**：一个 LLM 生成响应，另一个评估反馈循环

### Agents 核心三原则

1. **Simplicity** — 保持 Agent 设计简洁
2. **Transparency** — 通过显式展示 Agent 规划步骤保持透明
3. **ACI (Agent-Computer Interface)** — 通过充分的工具文档和测试精心设计工具

### Framework 建议

建议开发者先用 LLM API 直接实现（几行代码就能实现很多模式），框架会引入额外抽象层，可能掩盖底层 prompts，难以调试。

## 关键摘录

> "Success in the LLM space isn't about building the most sophisticated system. It's about building the *right* system for your needs."

> "We actually spent more time optimizing our tools than the overall prompt." — SWE-bench Agent 开发经验

## 相关实体

- [[claude-code|Claude Code]] — Anthropic 的 AI 编程工具
- [[anthropic|Anthropic]] — 发布此文的 AI 公司

## 相关概念

- [[ai-agent|AI Agent]] — 通用 Agent 概念
- [[mcp|MCP (Model Context Protocol)]] — Anthropic 提出的 Agent-工具连接标准
- [[multi-agent|Multi-Agent 系统]] — 多 Agent 协作
