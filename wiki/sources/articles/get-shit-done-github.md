---
title: GSD (Get Shit Done) — GitHub README
type: source
subtype: article
tags: [ai, context-engineering, multi-agent, claude-code]
created: 2026-04-24
updated: 2026-04-24
sources:
  - [[raw/articles/get-shit-done-github|原文]]
author: TÂCHES
url: https://github.com/gsd-build/get-shit-done
date: 2026-04
---

# GSD (Get Shit Done) — GitHub README

> GSD 是一个轻量级 meta-prompting + context engineering + spec-driven 开发系统，专为 Claude Code 设计，解决 context rot（上下文腐化）问题。56K+ Stars。

## 核心论点

1. **Context rot 是 AI 编码的根本问题**：随着对话积累，上下文越来越脏，生成质量下降。GSD 的解法是将大任务拆成可以在全新上下文窗口里独立完成的原子计划。
2. **Orchestrator 只调度，不执行**：主 Claude 实例保持 ~15% 上下文占用，所有繁重工作委托给子 Agent，每个子 Agent 享有完整的 200K token 新窗口。
3. **状态通过文件传递，不通过对话**：`CONTEXT.md`、`PLAN.md`、`STATE.md` 等文件是 Agent 间唯一的状态载体，彻底切断上下文污染链。
4. **Spec-first 开发**：先写规格（discuss → plan），再执行，避免 vibecoding 的不一致问题。

## 关键要点

- **Wave 并行执行**：plans 按依赖关系分组成 Wave，Wave 内并行、Wave 间串行。每个 plan 在独立的 `git worktree`（`isolation="worktree"`）里运行，文件系统完全隔离。
- **上下文隔离原语**：Claude Code 的 `Task()` API 为每次调用创建全新 Agent 实例；`isolation="worktree"` 进一步隔离文件系统，支持真正的并行修改。
- **Atomic commits**：每个任务完成后立即提交，可 `git bisect`，可独立 revert。
- **XML 结构化 plan**：`<task>/<action>/<verify>/<done>` 给 Claude 精确指令，内置验证条件。
- **多模型分层**：`quality` profile 用 Opus 规划 + Sonnet 执行，`budget` profile 全用 Sonnet/Haiku，可按成本需求切换。
- **安全内置**：路径遍历防护、prompt injection 检测、PreToolUse hook 扫描写入 `.planning/` 的内容。

## 提到的实体

- [[gsd|GSD（Get Shit Done）]] — 本工具
- [[taches|TÂCHES]] — 原作者

## 提到的概念

- [[concepts/ai/context-engineering|Context Engineering]] — GSD 的核心理念
- [[concepts/ai/multi-agent|Multi-Agent 系统]] — Wave 并行执行架构
- [[concepts/programming/spec-driven-development|Spec-Driven Development]] — discuss → plan → execute 工作流
