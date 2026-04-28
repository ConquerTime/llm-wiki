---
title: SWR
type: entity
subtype: product
tags: [tool, programming, frontend, server-state, open-source]
created: 2026-04-23
updated: 2026-04-23
sources:
  - ../../sources/articles/react-query-vs-swr-server-state-source-compare.md
---

# SWR

> 由 Vercel 开发的轻量 React 数据获取 hook 库，名称来自 HTTP 缓存策略 Stale-While-Revalidate——先返回缓存（可能过期），后台重新验证并更新。

## 基本信息

- **全称**：SWR（Stale-While-Revalidate）
- **开发者**：Vercel
- **主要包**：`swr`
- **当前主流版本**：v2.x
- **核心 API**：`useSWR(key, fetcher, config)`、`mutate(key, data?, options?)`

## 核心架构

```
cache provider（Map-like：key -> value）
  + per-key revalidator 列表

useSWR(key, fetcher)
  ├─ 读取缓存（立即展示 stale 数据）
  ├─ 触发 revalidate（后台 fetch）
  └─ 通过 useSyncExternalStore 订阅变化 -> re-render
```

- **key 序列化**：string/array/function 均可，内部序列化为字符串 cache key
- **去重策略**：`dedupingInterval` 时间窗内复用同一 in-flight promise
- **mutate**：`mutate(key)` 同时是写缓存（乐观更新）与触发 revalidate 的统一入口

## 设计哲学

SWR 把"协议复杂度"留给调用方或框架层（如 Next.js），自身保持极简。复杂 mutation orchestration 需团队自行约定领域封装层（如 `useUser()` / `useRepo()`）。

## 与本 wiki 的关联

- 是[[server-state-management|服务端状态管理]]主流方案之一
- 在源码层面与 [[tanstack-query|TanStack Query]] 进行了深度对比分析

## 出现的源摘要

- [[../../sources/articles/react-query-vs-swr-server-state-source-compare|React Query vs SWR 源码对比]]
