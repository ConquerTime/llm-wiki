---
title: "Lessons from building Claude Code: Prompt caching is everything"
type: source
author: Thariq Shihipar (Claude Code team)
url: "https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything"
date: 2026-05-08
created: 2026-05-10
updated: 2026-05-10
tags: [ai, engineering, tool]
sources:
  - ../../../raw/articles/Lessons from building Claude Code Prompt caching is everything.md
---

# Lessons from building Claude Code: Prompt caching is everything

> Prompt caching 是 Claude Code 高效运行的核心——通过前缀匹配复用计算，显著降低延迟和成本。

## 核心论点

Claude Code 团队分享了优化 prompt caching 的反直觉经验：

1. **Prompt caching 是前缀匹配**：前缀任何变化都会导致缓存失效，需要围绕这个约束设计整个系统
2. **静态在前，动态在后**：最佳排序是 Static System Prompt → CLAUDE.md → Session Context → Conversation Messages
3. **用 messages 而非修改 system prompt** 传递更新信息，避免 cache miss
4. **不要在对话中途切换模型或增删工具** — 这会破坏整个缓存
5. **缓存破坏要像监控 uptime 一样监控** — 几个百分点的 miss 率会显著影响成本和延迟

## 关键摘录

### Prompt 排序设计

```
1. Static system prompt + Tools (全局缓存)
2. CLAUDE.md (项目级缓存)
3. Session context (会话级缓存)
4. Conversation messages
```

### Plan Mode 的缓存安全设计

Claude Code 没有在进入 Plan Mode 时切换为只读工具集（这会破坏缓存），而是将 EnterPlanMode/ExitPlanMode 实现为工具本身，保持工具定义从不变化。

### 缓存安全的 Fork

Compaction（当上下文窗口满时对对话进行摘要）需要使用与父对话**完全相同的** system prompt、user context、system context 和 tool definitions，只在末尾添加一条 user message。这样 API 请求看起来与父请求几乎相同，复用缓存前缀。

## 相关实体

- [[claude-code|Claude Code]] — 构建此优化实践的 AI 编程工具

## 相关概念

- [[context-engineering|Context Engineering]] — 上下文窗口管理
- [[ai-agent|AI Agent]] — Agent 的 prompt caching 优化实践
