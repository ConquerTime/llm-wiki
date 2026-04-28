---
title: Context Engineering（上下文工程）
type: concept
subtype: ai
tags: [ai, context-engineering, multi-agent]
created: 2026-04-24
updated: 2026-04-24
sources:
  - ../../raw/articles/get-shit-done-github.md
---

# Context Engineering（上下文工程）

> 主动设计和管理 LLM 上下文窗口中的信息，以维持生成质量、避免 context rot 的工程实践。

## Context Rot 问题

LLM 的上下文窗口随任务积累越来越"脏"：已完成的讨论、调试历史、中间产物堆积，导致后期生成质量下降（变模糊、跳步骤、静默截断）。

**退化信号**：
- 开始用"appropriate handling"、"standard patterns"等模糊措辞替代具体代码
- 跳过本应执行的 protocol 步骤
- 声称任务完成但实现不完整

## 两种主要策略

### 1. 信息精选（What to load）

控制进入上下文的信息质量和数量：
- 只加载当前任务相关的文件
- 按上下文窗口大小决定读取深度（< 200K 只读 frontmatter，≥ 500K 可读全文）
- 用结构化文件（PROJECT.md、STATE.md、PLAN.md）代替散乱对话

### 2. 上下文隔离（Fresh context per task）

为每个子任务创建独立的、全新的上下文窗口：

**Claude Code 的实现原语**：

| 原语 | 作用 |
|------|------|
| `Task()` API | spawn 一个全新 Agent 实例，上下文从零开始 |
| `isolation="worktree"` | 为 Agent 创建独立 git worktree，文件系统完全隔离 |

**状态传递方式**：不通过对话传递，而通过磁盘文件：
```
Orchestrator ──读路径──► 子 Agent
                           └── 自己读 PLAN.md
                           └── 执行任务
                           └── 写 SUMMARY.md
                           └── 退出
```

## GSD 的 Context Budget 模型

[[gsd|GSD]] 明确量化了 context 分配：

| 角色 | Context 占用 | 职责 |
|------|-------------|------|
| Orchestrator | ~15% | 发现 plans、分析依赖、分组 Wave、spawn agents、收集结果 |
| 每个 Executor Agent | ~100%（全新） | 读 PLAN.md、执行任务、提交代码、写 SUMMARY.md |

**退化层级**（GSD context-budget.md 原文）：

| 层级 | 使用率 | 行为 |
|------|--------|------|
| PEAK | 0–30% | 正常操作，可读全文，可 spawn 多 agents |
| GOOD | 30–50% | 偏好 frontmatter 读取，积极委托 |
| DEGRADING | 50–70% | 节省模式，只读 frontmatter，警告用户 |
| POOR | 70%+ | 紧急模式，立即 checkpoint，不做新读取 |

## Wave 并行执行架构

```
Orchestrator（~15% context）
    │
    ├── Wave 1（并行）
    │   ├── Task(gsd-executor, isolation="worktree") → Plan 01 [全新 200K]
    │   └── Task(gsd-executor, isolation="worktree") → Plan 02 [全新 200K]
    │
    └── Wave 2（依赖 Wave 1 完成后并行）
        ├── Task(gsd-executor, isolation="worktree") → Plan 03 [全新 200K]
        └── Task(gsd-executor, isolation="worktree") → Plan 04 [全新 200K]
```

**顺序 dispatch**：worktree 创建需要加 git 锁（`.git/config.lock`），每次 `Task()` 调用必须逐一 dispatch（`run_in_background: true`），避免并发锁竞争；但 agents 一旦创建就真正并行运行。

## 文件驱动的状态管理

| 文件 | 内容 | 写入方 |
|------|------|--------|
| `PROJECT.md` | 项目愿景 | new-project |
| `CONTEXT.md` | 用户偏好决策 | discuss-phase |
| `RESEARCH.md` | 技术调研 | research agent |
| `PLAN.md` | 原子任务计划（XML） | planner agent |
| `STATE.md` | 当前项目状态 | SDK 维护 |
| `SUMMARY.md` | 任务完成报告 | executor agent |

## 开放问题

- 对于 1M token 窗口的模型（如 Gemini），是否还需要这么严格的隔离，还是可以更多地在单窗口内完成？
- 跨 Wave 的 SUMMARY.md 信息传递：1M 模型可以读取历史 SUMMARY，200K 模型只读 frontmatter——这个边界如何随模型进化？

## 来源

- [[sources/articles/get-shit-done-github|GSD GitHub README]]
