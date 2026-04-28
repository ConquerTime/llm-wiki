---
title: "OpenClaw + AI Agent 面试八股文：背完这篇，你懂的比面试官还多！"
type: source
subtype: article
tags: [ai, ai-agent, multi-agent, mcp, function-calling]
created: 2026-04-15
updated: 2026-04-15
sources:
  - ../../../raw/articles/OpenClaw + AI Agent 面试八股文：背完这篇，你懂的比面试官还多！.md
author: 王几行XING
url: https://zhuanlan.zhihu.com/p/2013536456132554764
date: 2026-03
---

# OpenClaw + AI Agent 面试八股文

> 一篇面向 AI Agent 工程师岗位的系统性八股文，以 OpenClaw 框架为主线，覆盖 Agent 核心架构、ReAct 框架、Function Calling、Multi-Agent 协议和安全机制，含 160+ 道分级面试题。

## 核心摘要

AI Agent 工程师岗位在 2026 年需求暴涨 25%。本文以 [[openclaw|OpenClaw]]（270K+ GitHub Stars 的开源 Agent 框架）为主线，系统讲解 AI Agent 工程师面试中最高频的八大主题。

**OpenClaw 的核心定位**：不是聊天工具，而是执行框架——"the AI that actually does things"。通过消息平台（WhatsApp/Telegram/飞书等 20+ 平台）接受指令，能发邮件、改文件、跑脚本、调 API。

## 关键要点

### OpenClaw 五大核心组件

1. **Gateway（网关）**：WebSocket 服务器（localhost:18789），负责消息路由。只做路由，不做推理——保证模块化，换平台不影响 Agent 逻辑。
2. **Brain（大脑）**：核心推理引擎，编排 LLM 调用，运行 ReAct 循环。模型无关，支持 GPT/Claude/Gemini/DeepSeek 等。
3. **Memory（记忆）**：全部用本地 Markdown 存储。两层架构：Daily Logs（`memory/YYYY-MM-DD.md`）+ MEMORY.md（长期记忆）。混合搜索：向量语义 + BM25 关键词。token 快用完时自动静默 flush。
4. **Skills（技能）**：存为 Markdown 文件的提示词模板，每个 Skill 一个文件夹含 `SKILL.md`。ClawHub 社区已有 5000+ Skills。
5. **Heartbeat（心跳）**：每 30 分钟触发一次，检查是否有需主动处理的任务。回复 `HEARTBEAT_OK` 则不通知用户（静默）。

### ReAct 框架

**ReAct = Reasoning + Acting**，推理与行动交替循环：

```
Thought → Action → Observation → 循环直到完成
```

与 CoT 的区别：CoT 只在模型内部推理（依赖内部知识，幻觉风险高）；ReAct 可通过 Action 调用外部工具获取真实数据，通过 Observation 验证推理，幻觉风险低。

> 面试金句："CoT 是让模型'想清楚'，ReAct 是让模型'想清楚然后动手干'。"

### AI Agent 四大基础组件

**Agent = LLM（大脑）+ Planning（规划）+ Memory（记忆）+ Tool Use（工具）**

- Planning 方法：CoT / ToT / Reflexion / Plan-and-Solve
- 记忆类型：短期（上下文窗口）/ 长期（向量数据库、Markdown 文件）
- 核心风险："幻觉-行动放大"——Agent 的幻觉不只是"说错话"，而会"做错事"

### Function Calling（工具调用）四步流程

1. 工具注册（定义 name/description/schema）
2. LLM 判断是否需要调用
3. 输出结构化 JSON 调用指令
4. 运行时执行并反馈结果

关键理解：**LLM 是"指挥官"，不是"执行者"**，执行由程序运行时负责。

### Multi-Agent 协议

| 协议 | 提出方 | 解决问题 | 类比 |
|------|--------|----------|------|
| MCP（Model Context Protocol）| Anthropic | Agent 如何连接工具/数据源 | USB 接口 |
| A2A（Agent-to-Agent Protocol）| Google/Linux基金会 | Agent 之间如何协作 | HTTP 协议 |

两者互补：MCP 管对外交互，A2A 管对内协作。

### OpenClaw vs 其他框架

| 框架 | 定位 | 适合场景 |
|------|------|----------|
| OpenClaw | 开箱即用的 Agent 应用 | 个人助手、快速原型 |
| LangChain/LangGraph | AI 应用开发积木 | 企业级 RAG、复杂流水线 |
| AutoGPT | 自主 Agent 实验项目 | 概念验证、学术研究 |

### 安全与 Guardrails

三大核心风险：Prompt Injection（间接注入更危险）、权限过大、数据泄露。

OpenClaw 内置防御：Pairing 认证、设备身份绑定、沙箱模式、工具权限策略。

安全原则（VISION.md）："Security is a deliberate tradeoff: strong defaults without killing capability"

## 提到的实体

- [[openclaw|OpenClaw]] — 本文主角，270K+ Stars 的开源 Agent 框架
- [[peter-steinberger|Peter Steinberger]] — OpenClaw 开发者
- [[langchain|LangChain]] — 对比框架：AI 应用开发积木
- [[autogpt|AutoGPT]] — 对比框架：自主 Agent 实验项目

## 提到的概念

- [[ai-agent|AI Agent]] — 自主执行任务的 AI 系统
- [[react-framework|ReAct]] — 推理与行动交替的 Agent 执行框架
- [[function-calling|Function Calling]] — LLM 与外部系统交互的工具调用机制
- [[multi-agent|Multi-Agent]] — 多 Agent 协作系统与协议
- [[mcp|MCP（Model Context Protocol）]] — Anthropic 提出的 Agent-工具连接标准协议
