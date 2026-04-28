---
title: Multi-Agent 系统与协议
type: concept
subtype: ai
tags: [ai, multi-agent, mcp]
created: 2026-04-15
updated: 2026-04-21
sources:
  - ../../raw/articles/OpenClaw + AI Agent 面试八股文：背完这篇，你懂的比面试官还多！.md
---

# Multi-Agent 系统与协议

> 多个独立 Agent 协作完成任务的系统，2026 年面试新热点，核心是 MCP 和 A2A 两大协议标准化。

## 两大核心协议

| 协议 | 全称 | 提出方 | 解决问题 | 类比 |
|------|------|--------|----------|------|
| MCP | Model Context Protocol | Anthropic | Agent 如何连接工具/数据源 | USB 接口 |
| A2A | Agent-to-Agent Protocol | Google / Linux 基金会 | Agent 之间如何协作 | HTTP 协议 |

**关系**：互补而非替代。MCP 管 Agent 对外交互，A2A 管 Agent 之间的团队协作。生产级系统通常两者都用。

### MCP 的核心价值

以前每接一个新工具都要写定制连接器，MCP 统一了接口——工具提供商实现 MCP Server，Agent 通过统一 MCP Client 接口连接，即插即用。

MCP Server/Client 模型：
- **MCP Server**：由工具提供商实现，暴露工具定义（name/description/schema）和执行端点
- **MCP Client**：集成在 Agent 中，负责发现可用 Server、发送调用请求、接收结果
- 通信协议：标准化 JSON-RPC

### 其他协议

2026 年五大 Agent 协议：MCP / A2A / ACP（Agent Communication Protocol）/ WebMCP / OpenAPI

## 常见架构模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| Supervisor | 中央调度器分配任务给 worker agents | 任务分工明确、需要中央协调 |
| Peer-to-peer | Agent 之间平等协作 | 能力对等、去中心化容错 |
| Hierarchical | 多层级的 supervisor 树 | 大规模复杂系统 |
| Swarm | 动态组队，按需加入退出 | 灵活协作 |

实际系统常混合使用：高层 Supervisor 分配，底层 worker 之间 Peer-to-peer。

## 核心挑战

1. **协调开销**：Agent 间通信消耗时间和 token
2. **一致性**：多 Agent 共享状态时的冲突
3. **故障传播**：一个 Agent 故障影响整体
4. **安全边界**：Agent 间的信任和权限管理
5. **可观测性**：调试分布式 Agent 行为困难

## OpenClaw 的 Multi-Agent 实现

[[openclaw|OpenClaw]] 支持在**一个 Gateway 进程中运行多个隔离的 Agent**。

隔离范围（每个 Agent 独立）：
- Workspace（文件系统、AGENTS.md/SOUL.md）
- Agent Dir（`~/.openclaw/agents/<agentId>/agent`，含 auth-profiles.json）
- Session Store（`~/.openclaw/agents/<agentId>/sessions/`）
- Skills（workspace `skills/`）

路由通过 `bindings` 配置：匹配条件（channel、account、peer 等）→ `agentId`

**安全模型**：OpenClaw 不将一个 Gateway 建模为多租户对抗性边界。推荐模式：一个用户一台机器/VPS，一个 Gateway，多个 Agent。

## 主要 Multi-Agent 框架（2026）

|| 框架 | 提出方 | 特点 |
|------|------|--------|------|
| [[openclaw|OpenClaw]] | OpenClaw | 本地优先、多 Agent 隔离运行 | 270K+ GitHub Stars |
| LangChain | LangChain | 企业级 RAG 和复杂 AI 流水线 | 成熟生态 |
| openai-agents-python | OpenAI | A lightweight, powerful framework for multi-agent workflows | 905 Stars，2026-04-21 |
| [[gsd|GSD（Get Shit Done）]] | TÂCHES | context engineering + spec-driven，Wave 并行执行，每 plan 独立上下文 | 56K+ Stars |

## Gartner 预测

预测到 2026 年，几乎每个商业应用都会有 AI 助手，其中 40% 会在次年集成任务特定的 Agent。

## 来源

- [[sources/articles/openclaw-ai-agent-interview|OpenClaw + AI Agent 面试八股文]]
- [[sources/morning-briefs/2026-04-21|晨报 2026-04-21]]
