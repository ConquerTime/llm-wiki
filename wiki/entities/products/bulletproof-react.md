---
title: Bulletproof React
type: entity
subtype: product
tags: [tool, react, architecture]
created: 2026-04-27
updated: 2026-04-27
sources:
  - "[[wiki/sources/articles/bulletproof-react-github.md|Bulletproof React 源摘要]]"
---

# Bulletproof React

> 一份意见性的 React 生产级架构指南 + 示例应用，GitHub 35k+ 星。不是模板、不是框架，而是"怎么把 React 项目组织好"的参考答案。

## 与本 wiki 的关联

- 作者：[[alan-alickovic|Alan Alickovic]]
- 仓库：<https://github.com/alan2207/bulletproof-react>
- 活跃度：2026 年持续更新
- 提出 [[feature-based-architecture|Feature-Based 架构]]——wiki 中"React 项目组织"的核心参考
- 提出 **React 状态五分类**（Component / Application / Server Cache / Form / URL）——[[react-page-state-antipatterns|React 页面状态反模式]] 的上位分类框架

## 包含内容

- 13 篇架构主题文档（项目结构、状态管理、API 层、错误处理、测试、安全、性能等）
- 3 个对等示例应用：
  - `apps/react-vite/` — Vite + React
  - `apps/nextjs-app/` — Next.js App Router
  - `apps/nextjs-pages/` — Next.js Pages Router

## 作者强调的"非目标"

> This is not supposed to be a template, boilerplate or a framework. It is an opinionated guide.

看这份指南时应聚焦**原则**而非具体工具选型，所用工具（react-query、zustand、zod 等）可以替换。

## 出现在

- [[wiki/sources/articles/bulletproof-react-github.md|Bulletproof React 源摘要]]
