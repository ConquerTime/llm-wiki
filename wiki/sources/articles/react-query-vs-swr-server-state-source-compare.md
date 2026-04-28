---
title: React Query vs SWR：服务端状态管理源码对比
type: source
subtype: article
tags: [programming, frontend, server-state]
created: 2026-04-23
updated: 2026-04-23
sources:
  - "[[../../raw/frontend/react/react-query-vs-swr-server-state-source-compare|原文]]"
---

# React Query vs SWR：服务端状态管理源码对比

> 从源码架构与运行时数据流出发，对比 TanStack Query（React Query）与 SWR 在缓存建模、组件订阅、请求去重/取消、失效与重新验证等核心设计上的差异与取舍。


## 核心论点

- 服务端状态的本质是管理"资源生命周期"，而非简单存值：`resource = data + metadata + in-flight + observers`。
- TanStack Query 以 `Query`/`QueryObserver` 作为资源实例，更像一个小型缓存与调度系统；SWR 以 `cache` + hook 协作，更像极简的 Stale-While-Revalidate runtime。
- 两者都正确使用了 `useSyncExternalStore` 避免 React 18 并发渲染下的 tearing 问题。
- 选型依据应从"状态语义"出发，而非 API 偏好：写多/复杂 mutation/DevTools 选 TanStack Query；读多/轻量缓存/低抽象选 SWR。
- 两者均不适合管理 UI 状态（modal、草稿、主题），那是 `useState`/Zustand 的领地。

## 关键要点

- **核心抽象差异**：TanStack Query 的 `Query` 是带状态机的资源实例，SWR 的 cache 是 `key -> value` 的 Map-like 结构。
- **queryKey vs key**：TanStack Query 用结构化数组 + hash 支持层级匹配（`invalidateQueries(['user'])` 失效整域）；SWR 序列化为字符串，需团队自己约定命名空间。
- **去重策略**：SWR 用时间窗 `dedupingInterval` 去重（时间窗外重新请求）；TanStack Query 用 Query 实例内聚 in-flight，多 observer 共享同一 fetch 生命周期。
- **新鲜度语义**：TanStack Query 的 `staleTime`（fresh/stale）与 `gcTime`（in-cache 保留）语义清晰可推导；SWR 依赖 provider 实现与分散的时间参数，需封装配置基线。
- **Mutation 一等公民**：TanStack Query 有 `MutationCache`、完整并发策略、lifecycle 钩子；SWR 的 `mutate` 足够覆盖 CRUD，但复杂 orchestration 需自己约定。
- **工程分层**：TanStack Query 的 `@tanstack/query-core` + adapter 分层易于跨框架复用与 DevTools 生态；SWR 更适合作为轻量数据获取 hook 标准层。

## 提到的概念

- [[server-state-management|服务端状态管理]]
- [[../../concepts/programming/observer-pattern|观察者模式]] — Observer/订阅模型
- React `useSyncExternalStore` — 并发安全外部 store 订阅
- Stale-While-Revalidate — HTTP 缓存策略，SWR 命名来源

## 提到的实体

- [[tanstack-query|TanStack Query（React Query）]]
- [[swr|SWR]]
