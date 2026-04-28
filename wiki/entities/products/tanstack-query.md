---
title: TanStack Query（React Query）
type: entity
subtype: product
tags: [tool, programming, frontend, server-state, open-source]
created: 2026-04-23
updated: 2026-04-24
sources:
  - ../../sources/articles/react-query-vs-swr-server-state-source-compare.md
---

# TanStack Query（React Query）

> 由 Tanner Linsley 创建的服务端状态管理库，以 `Query`/`QueryObserver` 为核心抽象，将服务端数据资源实体化为带状态机的实例，通过 `QueryClient` 统一调度缓存与订阅。

## 基本信息

- **正式名称**：TanStack Query（前身：React Query）
- **主要包**：`@tanstack/react-query`（React 绑定）、`@tanstack/query-core`（framework-agnostic 核心）
- **当前主流版本**：v5.x
- **支持框架**：React、Vue、Svelte、Solid（通过 adapter 分层）

## 核心架构

```
QueryClient
  ├─ QueryCache
  │    └─ Query（key -> 状态机：idle/loading/success/error）
  ├─ MutationCache
  └─ notifyManager / focusManager / onlineManager

React component
  └─ QueryObserver（订阅 Query -> 投影 result -> 触发 re-render）
```

- **Query**：管理数据、状态、时间戳、in-flight promise、retry、取消、GC
- **QueryObserver**：将 Query 状态投影为组件 result，支持 selector/config 差异化
- **MutationCache**：Mutation 作为一等公民，支持并发策略、retry、lifecycle 钩子

## 关键配置

- `staleTime`：数据被视为 fresh 的时长（内不触发 refetch）
- `gcTime`：无 observer 时 Query 在 cache 中保留时长
- `queryKey`：结构化数组，通过 hash 定位 Query 实例，支持层级匹配（`invalidateQueries(['user'])` 失效整域）

## 自动 refetch 触发时机

`useQuery` 在以下四种时机自动重新请求（数据已过期时）：

1. **组件挂载** — 挂载时如果数据是 stale，立刻请求
2. **窗口获得焦点** — 用户切换 Tab 再切回来（监听 `visibilitychange` / `focus` 事件）
3. **网络重新连接** — 断网再联网（监听 `window.addEventListener('online', ...)`）
4. **定时轮询** — 配置 `refetchInterval` 后每隔 N 秒自动请求

> 环境事件通过 `focusManager` / `onlineManager` 抽象为可替换模块，React Native 等非浏览器环境可自定义实现。

## 与本 wiki 的关联

- 是[[server-state-management|服务端状态管理]]主流方案之一
- 在源码层面与 [[swr|SWR]] 进行了深度对比分析

## 出现的源摘要

- [[../../sources/articles/react-query-vs-swr-server-state-source-compare|React Query vs SWR 源码对比]]
