---
title: AI Toolkit
type: synthesis
subtype: index
tags: [ai, tool]
created: 2026-05-09
updated: 2026-05-09
---

# AI Toolkit

> 我收藏的 AI / Agent / Skill 工具的 curation 索引。按**使用场景**分组，不按实现形态。事实卡片在 `entities/products/` 各自页面里，这里只做导航和评价。

## 使用约定

- 每一行格式：`[[条目]] — 一句话定位 · 状态标记`
- **状态标记**（手动维护）：`🟢 日常` / `🟡 试过` / `⚪ 待试` / `🔴 弃用`
- 新增 AI 工具类 entity 时顺手在这里登记一行
- 本页是 curation 视角，**条目可以同时出现在多个分组**（不必互斥）

---

## Claude Code Skills — 单技能 / 通用改进

- [[caveman-skill]] — 用原始人语言压缩 65% token · ⚪ 待标
- [[graphify]] — 把代码 / 文档转成知识图谱 · ⚪ 待标
- [[nuwa-skill]] — 思维蒸馏，六路 Agent 并行 + 三重验证 · ⚪ 待标
- [[andrej-karpathy-skills]] — Karpathy 版 CLAUDE.md 行为准则 · ⚪ 待标
- [[career-ops]] — 基于 Claude Code 的 AI 求职系统 · ⚪ 待标
- [[zhangxuefeng-skill]] — 高考 / 考研 / 职业规划思维框架 · ⚪ 待标

## Skills 合集 — 多 skill 打包

- [[superpowers]] — Agentic 技能框架与软件开发方法论 · ⚪ 待标
- [[mattpocock-skills]] — Matt Pocock 的实操 skills · ⚪ 待标
- [[khazix-skills]] — 数字生命卡兹克 AI Skills 合集 · ⚪ 待标
- [[browserbase-skills]] — Claude Agent SDK + 网页浏览 · ⚪ 待标
- [[greentrain-skills]] — 绿皮火车的 14 个 Claude Code skill 打包 · ⚪ 待标

## Agent 框架 / Harness / 编排

- [[gsd]] — context engineering + spec-driven 开发系统 · ⚪ 待标
- [[openclaw]] — 本地优先自主 AI Agent 框架 · ⚪ 待标
- [[gbrain]] — OpenClaw / Hermes 风格的 Agent Brain · ⚪ 待标
- [[ruflo]] — Claude 编排平台，支持 multi-agent swarms · ⚪ 待标
- [[roo-code]] — VS Code 内多智能体协同 · ⚪ 待标
- [[deepclaude]] — Claude Code agent loop + DeepSeek V4 Pro · ⚪ 待标
- [[autogpt]] — 早期自主 Agent 实验项目，偏研究 · ⚪ 待标

## Memory & Knowledge

- [[mempalace]] — 开源 AI memory system，Benchmark 领先 · ⚪ 待标
- [[graphify]]（重复列出）— 代码 / 文档→知识图谱 · ⚪ 待标

## 领域 Multi-Agent

- [[autoresearch]] — 自主 ML 实验，一夜 ~100 次 · ⚪ 待标
- [[tradingagents]] — 多智能体 LLM 金融交易框架 · ⚪ 待标

## LLM 框架 / SDK

- [[langchain]] — 企业级 RAG / Agent 编排积木 · ⚪ 待标

## 本地 / 终端客户端

- [[deepseek-tui]] — 终端运行的 DeepSeek 编程助手（Rust）· ⚪ 待标

## AI 设计系统

- [[open-design]] — 开源 Claude Design 替代，71 个设计系统 · ⚪ 待标

---

## 边界外（提醒自己不要混进来）

下列 entity 虽然挂 `tool` tag，但主要用途不是 AI 工具，不进本索引：
- 开发工具：[[obsidian]]、[[swr]]、[[tanstack-query]]、[[bulletproof-react]]、[[typescript-go]]、[[dav2d]]
- 产品 / 事件：[[posthog]]、[[vscode]]
- ML 训练基础设施：[[deepep]]（MoE 分布式训练，不是日常工具）

---

*维护规范：§6 wiki 规范。本页是 curation 性质的索引，条目的事实信息以 `entities/products/` 各自页面为准。*
