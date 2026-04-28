---
title: React 状态五分类
type: concept
subtype: programming
tags: [programming, react, state-management]
created: 2026-04-28
updated: 2026-04-28
sources:
  - "[[wiki/sources/articles/bulletproof-react-github.md|Bulletproof React]]"
---

# React 状态五分类

> 按**来源**而非"是否全局"把 React 应用中的状态拆成 Component / Application / Server Cache / Form / URL 五类，不同类用不同工具。这个分类是"避免所有东西塞 Redux"的起点，也是识别页面反模式时的上位框架。

## 是什么

大多数 React 项目的状态管理混乱都来自一个原始错误：**把所有状态看作同一类东西**，要么统统放 `useState` 要么统统放 Redux。实际上 React 应用里的"state"按**值的来源**可以分成五种：

| 分类 | 值从哪里来 | 典型工具 |
|------|----------|---------|
| **Component State** | 组件私有变量 | `useState` / `useReducer` |
| **Application State** | 跨组件共享的客户端状态 | Context + hooks / Zustand / Jotai / Redux Toolkit / XState |
| **Server Cache State** | 远端 API 的响应 | [[products/tanstack-query\|TanStack Query]] / [[products/swr\|SWR]] / Apollo / urql |
| **Form State** | 表单字段 | React Hook Form / Formik / Final Form（配合 zod/yup） |
| **URL State** | URL path / query / hash | react-router / Next.js router |

每类的管理语义不同，强行用同一套工具会出问题（见下）。

## 为什么重要

### 避免"Redux 塞一切"综合症

React 早期流行"单一 store 装一切"，服务端数据也被塞进 Redux。结果：
- 需要手写一整套 loading/error/refetch 逻辑
- 缓存失效、去重、后台刷新都要自己实现
- Redux 变成"有缓存能力的脏数据仓库"

**根因**：服务端数据是 Server Cache State，不是 Application State。来源不同，生命周期不同，就不该用同一套工具。

### 识别页面反模式的上位框架

[[react-page-state-antipatterns|React 页面状态管理反模式]] 里的"字段级三源合并"，本质是 URL State + Application State（sessionStorage）+ Application State（location.state）被字段级三元表达式合成一锅。**分类清楚之后，反模式 4 的解法**（单 hook 按源优先级一次性决定整对象）就自然出现。

### 指导工具选型

一个合理的生产级 React 项目通常这样组合：

- useState / useReducer（Component）
- [[server-state-management|服务端状态管理]]：TanStack Query（Server Cache）
- Zustand / Jotai（Application，轻量）
- React Hook Form + zod（Form）
- react-router（URL）

**不需要** Redux。Redux Toolkit + RTK Query 是另一种合理组合，但前者更轻量、更符合"工具贴合来源"的原则。

## 五类详解

### 1. Component State

**定义**：只被单个组件及其直接子组件需要的状态。

**判断标准**：能否"拎起这个组件塞到别的页面"还正常工作？能 → 是 component state。

**原则**：
- **从组件内部起**，按需上提（lifting state up）
- 不要预先全局化
- 复杂组合状态用 `useReducer` 而非多个 `useState`

典型例子：下拉菜单的 open/closed、tab 的当前选中项、modal 的打开状态。

### 2. Application State

**定义**：跨组件共享、属于客户端本地的状态。

**典型例子**：
- 全局通知（toast queue）
- 主题模式（dark/light）
- 用户偏好（侧边栏展开与否）
- 多步骤向导的跨步骤数据

**不属于这类**：
- 当前登录用户信息——看起来像 application state，但**本质是 Server Cache State**（值的权威来源在服务器）。用 react-query 管理，比放进 Zustand 合适得多。
- URL 参数——属于 URL State。

**工具光谱**：
- **小** — Context + hooks（纯 React，适合低频数据如主题）
- **中** — Zustand / Jotai（轻量 store，无 boilerplate）
- **重** — Redux Toolkit（生态成熟，DevTools 强）
- **状态机** — XState（有明确 phase 转移需求时）

### 3. Server Cache State

**定义**：客户端本地缓存的远端数据。权威来源在服务器，客户端只是镜像。

**特征**：
- 有新鲜度语义（staleTime / cacheTime）
- 需要去重（同一资源多组件订阅）
- 需要后台刷新、乐观更新、回滚
- 跨组件共享，但与业务 state 机制不同

详见 [[server-state-management]]——本分类是那一页的上位框架。

### 4. Form State

**定义**：表单字段值、校验结果、提交状态。

**为什么需要独立工具**：
- 原生 React 做表单需要大量样板（controlled input、onChange、校验、错误映射）
- 重渲染问题：每次输入都触发整个表单重渲染
- React Hook Form 通过 uncontrolled + ref 避开重渲染，性能明显更好

**工具选型**：
- **首选** React Hook Form + zod（性能 + 类型安全）
- **旧项目** Formik（更老，但仍在维护）
- **特殊** Final Form（订阅级粒度控制）

### 5. URL State

**定义**：存储在 URL 中的状态——path params、query params、hash。

**关键认知**：URL State 是**可分享、可刷新、可收藏**的状态。任何应该满足这三条的状态都应该放 URL，而不是 Application State。

**典型例子**：
- 列表页的当前页码、筛选条件、排序字段 → **全部应放 query string**
- 详情页的资源 id → path param
- tab 页的当前 tab → query param（这样分享链接能定位到同一 tab）

**反模式**：把筛选条件放 Zustand 或 useState。用户复制 URL 给同事，对方打开看不到同样的过滤结果。

## 分类边界的常见困惑

### 当前登录用户信息算哪类？

权威来源在服务器 → **Server Cache State**。用 `useQuery(['user'])` 管理。

作者 Alickovic 的 `react-query-auth` 库就是这个思路的落地——认证状态不进全局 store，而是进 react-query 的缓存。

### Modal 开关状态算哪类？

- 只当前页面用 → Component State
- 多页面需要控制（如全局确认对话框） → Application State
- 能被 URL 定位（`?modal=share`） → URL State（**推荐**，可分享可刷新）

### 向导（wizard）多步骤数据算哪类？

- 只在向导内流转 → Application State（Context 或 Zustand）
- 允许用户刷新继续 → URL State（step 放 path，数据放 sessionStorage）+ Application State 的组合

## 常见误区

### 误区 1：把 Server Cache 塞进 Redux/Zustand

后果：
- 重造 react-query 的轮子（且不如它好）
- 多处组件各自触发 fetch，没有去重
- staleTime / gcTime 没有，数据永远新鲜或永远过期

### 误区 2：所有东西都用 Context

Context 适合**低频、低速度**的数据（主题、用户信息）。高频更新（如鼠标位置、输入值）放 Context 会让所有消费者重渲染。

解法：小 store（Zustand/Jotai）或 `use-context-selector`。

### 误区 3：Form State 用 useState 纯手写

在超过 3 个字段 + 校验的表单上，纯手写很快就失控。应该直接上 React Hook Form。

### 误区 4：忘了 URL State

最常见的反模式：列表页的筛选器/分页用 useState 管理。用户刷新页面就丢、分享链接给同事打开状态不一致。

**判断**：如果某个状态应该满足"分享/刷新/收藏"中的任何一条 → 放 URL。

## 与相关模式的关系

- [[react-page-state-antipatterns|React 页面状态管理反模式]] — 本分类是其上位框架，页面反模式的根源往往是"多类 state 混成一锅"
- [[server-state-management|服务端状态管理]] — Server Cache State 的深入讨论
- [[feature-based-architecture|Feature-Based 架构]] — 模块级组织框架，本分类是状态级组织框架

## 开放问题

- **Next.js App Router 的 Server Components 之后，Application State 的边界如何变？** 部分原本的 Application State 可以上移到 Server Components，变成 Server Cache State。这会让 client bundle 更小，但跨 feature 共享客户端状态的场景依然存在。
- **React 19 的 `useActionState` / Form Actions 会吞噬 Form State 工具吗？** 目前看：简单表单用原生 Action 够用，复杂表单（字段联动、复杂校验）React Hook Form 仍更合适。
- **URL State 的 type safety？** nuqs、next-usequerystate 等库开始给 query params 加 TypeScript 类型，这是目前最弱的一环。

## 来源

- [[wiki/sources/articles/bulletproof-react-github.md|Bulletproof React]] — 最早把五分类清晰化的公共文档之一
