---
title: "Context, Not Control"
type: source
subtype: article
tags: [ai]
author: VM0
source: raw/articles/Context, Not Control.md
url: https://www.vm0.ai/en/blog/posts/context-not-control-1
date: 2026-04-14
created: 2026-05-06
updated: 2026-05-06
sources:
  - "../raw/articles/Context, Not Control.md"
---

# Context, Not Control

> AI Agent 的 system prompt 不应该是官僚制度，而应该是让 agent 理解所处的环境。

## 核心论点

Agent 的 system prompt 中积累的规则（"never do X"、"avoid Y"）是**控制式思维**的体现——看到错误行为就加规则，而不解决根本问题。正确的方式是**上下文式思维**：给 agent 提供关于环境、权限、范围的真实事实，让 agent 自己推理。

**启发式原则**：每当你想在 prompt 里写 "don't"、"avoid"、"never" 时，停下来问自己——这条规则在补偿哪个缺失的事实？写出那个事实，删除那条规则。

## 关键摘录

> Every rule in your agent's prompt started as a bug.

> The first approach patches one behavior. The second gives the agent a model of the situation. Now it can reason about nearby questions too.

> A fact like "this run was triggered by a scheduled task at 3 AM" is stable. A statement like "you should avoid creating sub-schedules" is fragile.

> Teams constantly turn temporary model defects into permanent system structure.

> Documenting stable system behavior is valuable. Patching a model's reasoning tendencies is a treadmill.

## 控制式 vs 上下文式示例

**控制式**：
> TOKEN is missing. Run "zero permissions request gmail.send" to fix it.

**上下文式**：
> process.env.GMAIL\_TOKEN → exists zero connectors inspect gmail → connected zero permissions inspect gmail.send → denied
> Options: 1) Request user approval 2) Use already-authorized path

## 设计原则

1. **事实比观点更稳定** — 事实跨模型通用，"应该/避免"依赖于模型推理倾向
2. **规则是代理（proxy）** — 规则不是目标本身，规则会堆积成官僚主义
3. **不要把模型 quirks 固化成系统结构** — 模型会变，规则补丁会成为遗留代码
4. **硬边界仍然必要** — 破坏性操作、金钱移动、安全边界需要真实约束

## 与本 wiki 的关联

- [[context-engineering|Context Engineering]] — 本文是"context over control"哲学的实践文章
- [[agent-harness|Agent Harness]] — harness 负责提供环境上下文，与本文核心思想高度相关
- [[ai-agent|AI Agent]] — prompt engineering 是 agent 设计的核心议题

## 提到的实体

- [[your-harness-your-memory|Your Harness, Your Memory]] — LangChain CEO 文章，harness 与 memory 不可分割

## 提到的概念

- [[context-engineering|Context Engineering]]
- [[agent-harness|Agent Harness]]
- [[ai-agent|AI Agent]]
