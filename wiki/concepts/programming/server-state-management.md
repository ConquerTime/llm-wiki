---
title: 服务端状态管理（Server State Management）
type: concept
subtype: programming
tags: [programming, frontend, server-state]
created: 2026-04-23
updated: 2026-04-27
sources:
  - "[[../../sources/articles/react-query-vs-swr-server-state-source-compare|React Query vs SWR 对比]]"
  - "[[../../sources/articles/bulletproof-react-github|Bulletproof React]]"
---

# 服务端状态管理（Server State Management）

> 管理来自网络/数据库等外部来源的异步数据的生命周期，核心是处理缓存、新鲜度、去重、失效与一致性，而非"存一个值"。

## 核心定义

服务端状态与客户端 UI 状态有本质区别：

- **来源不在客户端**：值来自网络、数据库、Edge、第三方 API
- **有新鲜度语义**：同一资源在不同时间段可能"足够新"或"必须刷新"
- **需要一致性策略**：去重、取消、重试、失效、后台刷新、乐观更新、回滚
- **跨组件共享**：多组件读取同一资源，各自可在不同生命周期触发刷新

因此其本质是管理**资源生命周期**：

```
resource = data + metadata + in-flight + observers
```

## 两大主流方案对比

| 维度 | [[tanstack-query|TanStack Query]] | [[swr|SWR]] |
|---|---|---|
| 核心抽象 | `Query`/`QueryObserver`（资源实例 + 状态机） | `cache` Map + `useSWR` hook |
| 缓存容器 | `QueryCache`（以 Query 实例为单位） | cache provider（key -> value） |
| 新鲜度语义 | `staleTime`（fresh/stale）+ `gcTime`（GC）清晰分离 | `dedupingInterval` + provider 策略，语义分散 |
| 请求去重 | Query 实例内聚 in-flight，多 observer 共享 | 时间窗 `dedupingInterval`，窗口外重新请求 |
| 失效方式 | `invalidateQueries(['key'])` 声明式标记 stale | `mutate(key)` 直接触发 revalidate |
| Mutation | `MutationCache`，一等公民，完整并发控制 | `mutate()` 足够覆盖 CRUD，复杂场景需自约定 |
| 工程分层 | `query-core` + adapter，跨框架 + DevTools 生态 | 轻量 hook 标准层，适合 Next.js 轻量场景 |

## 关键机制

### 新鲜度（stale/fresh）

"新鲜"指数据在 `staleTime` 内不触发 refetch；超时后变为 stale，下次 mount/focus 时重新验证。这是 SWR 设计哲学的核心——"先展示缓存，后台刷新"。

### 去重（Deduplication）

同一资源被多个组件同时请求时，应只发出一次网络请求，结果共享给所有订阅者。TanStack Query 通过 Query 实例实现；SWR 通过时间窗实现。

### 失效（Invalidation）

mutation 成功后，需要告知系统相关缓存已过期、需重新获取。TanStack Query 的失效是"状态标记"（不立即请求），活跃 observer 按需触发 refetch，便于节流与批处理。

### 渲染一致性

React 18 并发渲染下，外部 store 订阅须用 `useSyncExternalStore` 避免 tearing（不同 fiber 读到不同版本的外部状态）。两者均已采用此模式或等价实现。

## 选型决策

**选 TanStack Query：**
- 需要明确的 fresh/stale/GC 语义可推导
- 有大量复杂 mutation（乐观更新、回滚、并发控制）
- 需要 DevTools、持久化、分页/无限滚动
- 希望把服务端状态层作为团队基础设施

**选 SWR：**
- 读多写少，轻量缓存场景
- 更倾向把复杂性收口到框架/领域层
- 希望最少抽象与 bundle 开销

## 边界：不适合管理的状态

UI 状态（主题、modal 开关、草稿输入、交互步骤）**不应**放入服务端状态缓存。这类状态应由：
- `useState`/`useReducer`（组件内）
- Zustand/Jotai/Redux（客户端跨组件共享）

负责。混入服务端状态缓存会导致语义错乱与维护成本飙升。

**服务端数据也不应放 Zustand/Redux。** `QueryCache` 是全局单例，同一 `queryKey` 在任何层级的组件里调用 `useQuery` 都共享同一份缓存和同一次请求，无需手动"抬升到全局状态"。把 API 数据放进 Zustand 是多此一举，且引入了手动同步的负担。

## 相关概念

- [[react-state-categories|React 状态五分类]] — 本页是其中"Server Cache State"一类的深入展开
- [[react-page-state-antipatterns|React 页面状态管理反模式]] — 当 Server Cache 与 URL/Application State 混用时产生的问题

## 来源

- [[../../sources/articles/react-query-vs-swr-server-state-source-compare|React Query vs SWR 源码对比]]
- [[../../sources/articles/bulletproof-react-github|Bulletproof React]]
