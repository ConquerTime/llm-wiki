---
title: MCP（Model Context Protocol）
type: concept
subtype: ai
tags: [mcp, protocol, anthropic, tool-use, agent-infrastructure]
created: 2026-04-15
updated: 2026-04-15
sources:
  - ../../raw/articles/OpenClaw + AI Agent 面试八股文：背完这篇，你懂的比面试官还多！.md
---

# MCP（Model Context Protocol）

> Anthropic 提出的通用适配器协议，标准化 Agent 与工具/数据源的连接方式，让任何工具提供商只需实现一个标准接口，所有 Agent 即可即插即用。

## 核心价值

以前每接入一个新工具都需要写定制连接器，MCP 统一了这个接口——类比 USB：以前每个外设（键盘、鼠标、打印机）有专用接口，USB 统一了它们。

## Server/Client 模型

- **MCP Server**：由工具提供商实现，暴露工具定义（name/description/schema）和执行端点
- **MCP Client**：集成在 Agent 中，负责发现可用 Server、发送调用请求、接收结果
- 通信协议：标准化 JSON-RPC

## 与 A2A 的关系

MCP 和 A2A 互补而非替代，共同构成 [[multi-agent|Multi-Agent]] 基础设施层：

| 协议 | 解决问题 | 类比 |
|------|----------|------|
| MCP | Agent 如何连接工具/数据源（对外）| USB 接口 |
| A2A | Agent 之间如何协作（对内）| HTTP 协议 |

## 来源

- [[sources/articles/openclaw-ai-agent-interview|OpenClaw + AI Agent 面试八股文]]
