---
title: Your harness, your memory
type: source
subtype: article
author:
  - Harrison Chase
url: https://www.langchain.com/blog/your-harness-your-memory
date: 2026-04-12
created: 2026-05-01
updated: 2026-05-01
tags: [ai, agent, memory]
sources:
  - ../../../raw/articles/Your harness, your memory.md
---

> Agent harnesses are becoming the dominant way to build agents, and they are intimately tied to agent memory. If you use a closed harness behind a proprietary API, you are yielding control of your agent's memory to a third party.

## 核心论点

LangChain CEO Harrison Chase 论点是：**Agent 的 harness（控制框架）与 memory（记忆）是不可分割的**。Harness 负责管理上下文，而上下文就是短期记忆和长期记忆的载体。闭源 harness（即闭源框架）会将 memory 锁死在单一平台，造成供应商锁定。

## 关键摘录

### 1. Agent Harnesses 的崛起

- 2023-2024：RAG chains → LangGraph → **Agent Harnesses**
- 代表产品：Claude Code、Deep Agents、Pi（OpenClaw 背后）、OpenCode、Codex、Letta Code
- 512k 行 Claude Code 泄露代码证明：即使是最好的模型提供商，也在大量投资 harness 开发

### 2. Memory is the Harness

引用 Sarah Wooders（Letta CTO）的观点：

> "Asking to plug memory into an agent harness is like asking to plug driving into a car."

Harness 负责的事情天然包括 memory：
- AGENTS.md / CLAUDE.md 文件如何加载
- Skill metadata 如何展示给 Agent
- Agent 能否修改自己的 system prompt
- Compaction 后什么保留、什么丢失
- 交互历史如何存储和查询

### 3. 供应商锁定的三个等级

| 等级 | 问题 | 例子 |
|------|------|------|
| 轻度 | 有状态 API，线程无法跨模型迁移 | OpenAI Responses API |
| 中度 | 闭源 harness，memory 格式不透明 | Claude Agent SDK |
| 重度 | 整个 harness + memory 都在 API 后面 | Anthropic Managed Agents |

### 4. Memory 重要性

- **无 memory**：Agent 容易被复制（谁能访问相同工具，谁就能复制）
- **有 memory**：构建专有数据集，形成差异化体验
- 情感案例：作者自己的邮件助手被误删后体验断崖下跌

### 5. Open Memory, Open Harnesses

LangChain 的 Deep Agents 方案：
- 开源、模型无关
- 使用 open standards：agents.md、skills
- 支持 Mongo/Postgres/Redis 作为 memory store
- 可自托管

## 提到的实体

- [[openclaw|OpenClaw]] — Pi agent 的底层框架
- [[langchain|LangChain]] — 文章作者所在公司
- [[mempalace|MemPalace]] — 48K Stars 的 AI memory system benchmark 表现最佳
- Letta — 前 Virtual 团队，stateful agents 前沿
- [[autoresearch|autoresearch]] — Karpathy 的自主 ML 研究框架（提及为 harness 例子）

## 提到的概念

- [[ai-agent|AI Agent]] — harness 是构建 agent 的脚手架
- [[context-engineering|Context Engineering]] — memory 是 context 的一种形式
- [[multi-agent|Multi-Agent 系统]] — 多 agent 协作时 memory 管理更复杂
