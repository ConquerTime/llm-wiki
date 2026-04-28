---
title: Spec-Driven Development
type: concept
subtype: programming
tags: [programming, workflow]
created: 2026-04-28
updated: 2026-04-28
sources:
  - "[[../../../raw/articles/get-shit-done-github|原文]]"
---

# Spec-Driven Development

> 先写规格说明（Spec），再写实现代码。Spec 是任务的合同，也是多 Agent 协作的界面。

## 概述

Spec-Driven Development（SDD）是一种工作流方法论，核心思想是：**在写代码之前先写规格说明**。规格说明定义了"成功长什么样"，是验收测试的源头，也是多 Agent 协作时的通信协议。

典型工作流：

```
discuss → plan → spec → execute → verify → ship
```

GSD 系统中的 `gsd-planner` Agent 负责生成 Spec，`gsd-executor` 负责实现，`gsd-verifier` 负责验收。

## 关键特征

- **Spec 先于实现**：代码是 Spec 的实现，不是 Spec 适配代码
- **验收驱动**：Spec 是验收测试的来源
- **多 Agent 界面**：Spec 是不同 Agent 之间传递上下文的标准格式
- **Context 隔离**：每个 plan 在全新 200K token 上下文窗口里执行

## 相关概念

- [[concepts/ai/context-engineering|Context Engineering]] — 通过 Task() API + worktree 隔离实现上下文隔离
- [[concepts/programming/observer-pattern|Observer Pattern]] — 状态变化通知机制

## 来源

- [[sources/articles/get-shit-done-github|GSD GitHub README]]
