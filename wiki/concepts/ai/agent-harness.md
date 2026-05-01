---
title: Agent Harness
type: concept
subtype: ai
tags: [ai, agent, memory]
created: 2026-05-01
updated: 2026-05-01
sources:
  - [[../../sources/articles/your-harness-your-memory|LangChain Blog: Your harness, your memory]]
---

> Agent Harness 是构建 AI Agent 的控制框架，负责管理 Agent 的上下文、记忆和工具调用，是 Agent 系统的"脚手架"。

## 定义

Harness（控制框架）是围绕 LLM 的系统层，负责：
- 管理**短期上下文**（对话消息、工具调用结果）
- 管理**长期记忆**（跨会话状态、用户偏好）
- 协调**工具调用**（tool use、function calling）
- 加载**系统指令**（AGENTS.md、CLAUDE.md 等）

Harness 与 Memory 不可分割——管理上下文就是管理记忆，正如汽车管理燃油系统是天然职责而非可选附件。

## 核心产品

| 产品 | 类型 | 说明 |
|------|------|------|
| [[openclaw|OpenClaw]] | 开源 | Pi agent 底层，270K Stars |
| [[langchain|LangChain]] / LangGraph | 开源 | 企业级 RAG +复杂流水线 |
| Claude Code | 闭源 | Anthropic 官方 Agent SDK，512K 行源码泄露 |
| Deep Agents | 开源 | LangChain 的 harness 项目，模型无关 |
| [[autoresearch|autoresearch]] | 开源 | Karpathy 极简 harness，三文件设计 |
| Letta Code | 闭源 | Letta 的 code agent，stateful |

## 供应商锁定风险

使用闭源 harness（尤其是将 memory 也闭源）会造成三层锁定：

1. **轻度**：有状态 API，线程无法跨模型迁移
2. **中度**：闭源 harness，memory 格式不透明
3. **重度**：整个 harness + memory 在 API 后，完全不可控

闭源模型提供商（Anthropic、OpenAI）有强烈动机将 harness 和 memory 锁定在平台内，形成数据飞轮护城河。

## 记忆类型

| 类型 | 载体 | 管理方 |
|------|------|--------|
| 短期记忆 | 对话消息、工具结果 | Harness |
| 长期记忆 | 跨会话用户偏好、历史 | Harness |
| 压缩摘要 | Compaction 结果 | Harness（如 Claude Code） |
| 外部存储 | Redis/PG/Mongo 等 | Open harness 可接入 |

## 与 Context Engineering 的关系

[[context-engineering|Context Engineering]] 是 harness 的核心职责之一。[[ai-agent|AI Agent]] 通过 harness 与世界交互，harness 的设计直接影响 Agent 的推理质量和行为一致性。

参见 [[ai-agent]] 了解更多 Agent 架构，以及 [[context-engineering]] 了解如何管理上下文。

## 开放标准

行业正在形成 open harness 标准：
- **agents.md** — Agent 系统提示规范
- **skills**（agentskills.io）— Agent 技能定义规范
- **MCP** — [[mcp|Model Context Protocol]]，Anthropic 提出的工具连接标准

## 争议与开放问题

- 模型提供商是否会将 memory 完全吸收进 API？
- 独立的 memory 系统是否有未来，还是必然被 harness 整合？
- Open harness 的性能是否会永远落后于闭源集成方案？
