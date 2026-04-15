---
title: OpenClaw
type: entity
subtype: product
tags: [ai-agent, open-source, nodejs, typescript]
created: 2026-04-15
updated: 2026-04-15
sources:
  - ../../../raw/articles/OpenClaw + AI Agent 面试八股文：背完这篇，你懂的比面试官还多！.md
---

# OpenClaw

> 开源本地优先的自主 AI Agent 框架，270K+ GitHub Stars，通过消息平台让大模型代替用户执行真实任务。

## 基本信息

- **前身名称**：Warelay → Clawdbot → Moltbot → OpenClaw
- **开发者**：[[peter-steinberger|Peter Steinberger]]
- **许可证**：MIT License
- **技术栈**：Node.js v22+，TypeScript
- **GitHub**：270K+ Stars

## 与本 Wiki 的关联

OpenClaw 是 2026 年 AI Agent 工程师面试中最高频考察的框架，代表了"执行优先"的 Agent 设计理念——不只是对话，而是真正替用户干活。

**核心差异化**：

| 特点 | 说明 |
|------|------|
| 开源本地优先 | MIT 许可，数据存本地 Markdown，不依赖云端数据库 |
| 多平台接入 | 原生支持 20+ 消息平台（WhatsApp/Telegram/Slack/飞书等）|
| 自主执行 | 能执行 shell 命令、浏览器自动化、文件操作 |

## 五大核心组件

1. **Gateway** — WebSocket 路由服务器（localhost:18789），只做路由不做推理
2. **Brain** — ReAct 推理引擎，模型无关（GPT/Claude/Gemini/DeepSeek 均支持）
3. **Memory** — 本地 Markdown 文件存储，混合搜索（向量 + BM25）
4. **Skills** — Markdown 提示词模板，ClawHub 已有 5000+ 社区 Skills
5. **Heartbeat** — 每 30 分钟主动检查，实现 Agent 主动执行

## 配套生态

- **Companion App**：macOS/iOS/Android 原生客户端，提供摄像头/位置/屏幕录制等设备能力
- **Canvas/A2UI**：Agent 驱动的可视化工作区
- **ClawHub**：Skills 社区市场
- **Swabble**：Swift 语音唤醒模块

## 出现在以下源摘要

- [[sources/articles/openclaw-ai-agent-interview|OpenClaw + AI Agent 面试八股文]]
