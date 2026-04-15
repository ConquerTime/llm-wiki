---
title: Karpathy Guidelines
type: concept
subtype: programming
tags: [karpathy, guidelines, coding, best-practices]
created: 2026-04-14
updated: 2026-04-15
sources:
  - ../../raw/articles/llm-wiki-by-karpathy.md
---

# Karpathy Guidelines

> [[andrej-karpathy|Karpathy]] 提出的四条 LLM 编程行为准则：思考、简单、精准、验证。

## 背景

这组准则来自 Karpathy 在 Twitter 上的观察，针对的是 LLM Agent 在编码时常犯的错误：过度工程、静默假设、修改范围膨胀、缺乏验证。准则偏向谨慎而非速度，适合 LLM 辅助编程和知识库维护场景。

## 四条准则

### 1. 编码前先思考 (Think Before Coding)

**不要假设。不要隐藏困惑。呈现权衡。**

- 明确陈述假设，不确定就问
- 多种解释全部呈现，不静默选择
- 有更简单方案就指出

### 2. 简单优先 (Simplicity First)

**最小代码解决问题。不做推测性代码。**

- 不添加超出需求的功能和抽象
- 检验标准："一个高级工程师会说这太复杂了吗？"

### 3. 精准修改 (Surgical Changes)

**只触碰必须改的。只清理自己造成的混乱。**

- 不"改进"相邻代码，不重构没坏的东西
- 匹配现有风格
- 每一行修改都应直接追溯到用户需求

### 4. 目标驱动执行 (Goal-Driven Execution)

**定义成功标准。循环直到验证通过。**

- 将任务转化为可验证目标
- 多步骤任务先列计划和检查点

## 来源

- [[sources/articles/llm-wiki-by-karpathy|Karpathy 2026]]
