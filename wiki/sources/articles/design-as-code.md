---
title: "Design-as-code: how we rebuilt our entire platform in 12 days"
type: source
subtype: article
tags: [programming]
author: VM0 (Yuma)
source: raw/articles/Design-as-code how we rebuilt our entire platform in 12 days.md
url: https://www.vm0.ai/en/blog/posts/design-as-code
date: 2026-04-29
created: 2026-05-06
updated: 2026-05-06
sources:
  - "../raw/articles/Design-as-code how we rebuilt our entire platform in 12 days.md"
---

# Design-as-code

> 产品设计师用 AI 工具直接输出 React 代码，前端工程师负责架构扩展和质量把关。12 天完成 26,000 行遗留代码的平台重建。

## 核心论点

传统设计-工程协作的瓶颈不在于任何一个单独步骤，而在于**步骤之间的间隙**：等待、翻译损耗、上下文切换。AI 工具消除了设计与工程之间的翻译层——设计师用 AI 直接输出代码，工程师在原地扩展架构。

**核心变化**：设计师不再输出 Figma 文件，而是输出 React 代码；工程师不再做视觉翻译，而是做架构扩展。

## 关键数据

- **12 天** — 从第一个脚手架到完整平台替换
- **26,041 行删除** — 单次 PR，-26,041 / +456
- **914 个合并 PR**（679 工程师 + 235 设计师）
- **88%** 的工程师 PR 和 **66%** 的设计师 PR 有 AI 共同署名
- **48 小时** — 完成 Telegram 集成（最快功能）

## 工作流分工

| 角色 | 传统工作 | AI 时代工作 |
|------|----------|------------|
| **设计师（Ming）** | Figma 画图 → 标注 → 交接 | AI 直接生成 React 代码 → PR |
| **工程师（Yuma）** | 视觉翻译 → 像素对标 | 架构扩展 → API 集成 → 数据流 |

## AI 的真实角色

- **AI 赋能设计师写代码** — Cursor / Claude Code 处理机械翻译（JSX、CSS、组件组合），设计师负责视觉和交互决策
- **AI 加速评审循环** — AI agent 分类 P0/P1/P2 问题，38 分钟完成 5 轮评审
- **AI 不做设计决策** — 信息架构、交互模式、视觉层级来自设计师的产品直觉
- **AI 不做架构决策** — Feature Flag 策略、API 分层策略、增量连接策略是工程判断

## 关键工程实践

- **Feature Switch** — `FeatureSwitchKey.Zero` 实现新旧平台并行，5 天全路径验证后才切换
- **渐进式连接** — 页面骨架 → API 连接 → 真实数据，步步可回滚
- **无数据迁移** — 新旧系统共享同一后端，前端替换而非数据迁移

## 与本 wiki 的关联

- [[coding-agent|Coding Agent]] — AI 辅助编程的核心案例，设计师直接用 AI 写代码
- [[design-patterns|设计模式]] — 涉及 Feature Flag 模式（金丝雀部署的变体）
- [[feature-based-architecture|Feature-Based 架构]] — 平台按功能模块增量构建

## 提到的实体

- [[caveman-skill|caveman]] — GitHub 54.7K Stars，token压缩65%

## 提到的概念

- [[coding-agent|Coding Agent]]
- [[design-patterns|设计模式]]
- [[feature-based-architecture|Feature-Based 架构]]
- [[canary-deployment|金丝雀部署]]（Feature Flag 模式）
