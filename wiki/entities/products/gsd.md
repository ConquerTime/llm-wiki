---
title: GSD（Get Shit Done）
type: entity
subtype: product
tags: [tool, claude-code, context-engineering, multi-agent]
created: 2026-04-24
updated: 2026-04-24
sources:
  - [[raw/articles/get-shit-done-github|原文]]
---

# GSD（Get Shit Done）

> 轻量级 meta-prompting + context engineering + spec-driven 开发系统，专为 Claude Code 设计，解决 context rot 问题。56K+ GitHub Stars。

## 基本信息

- **作者**：TÂCHES
- **仓库**：https://github.com/gsd-build/get-shit-done
- **安装**：`npx get-shit-done-cc@latest`
- **Stars**：56K+（2026-04-24）
- **License**：MIT
- **支持运行时**：Claude Code、OpenCode、Gemini CLI、Codex、Copilot、Cursor、Windsurf 等

## 与本 wiki 的关联

GSD 系统性地解决了 AI 辅助编码中 context rot 问题，核心机制是通过 Claude Code 的 `Task()` API + `isolation="worktree"` 参数实现上下文隔离——每个 plan 在全新 200K token 上下文窗口里执行，状态通过文件系统（而非对话）在 Agent 间传递。

实现原理见 [[concepts/ai/context-engineering|Context Engineering]] 概念页。

## 工作流程

```
discuss-phase → plan-phase → execute-phase → verify-work → ship
```

每个阶段由专用 Agent 类型处理（`gsd-executor`、`gsd-verifier`、`gsd-planner` 等）。

## 出现在哪些源摘要中

- [[sources/articles/get-shit-done-github|GSD GitHub README]]
