---
title: React 架构栈
type: synthesis
tags: [programming, react, architecture]
created: 2026-04-28
updated: 2026-04-28
sources:
  - "[[wiki/sources/articles/bulletproof-react-github.md|Bulletproof React]]"
  - "[[wiki/sources/articles/react-bits-github.md|React Bits]]"
  - "[[wiki/sources/articles/react-query-vs-swr-server-state-source-compare.md|React Query vs SWR 源码对比]]"
---

# React 架构栈

> React 官方只给了一个渲染引擎；一个**可维护**的 React 应用需要在它之上手动叠加六层架构——组织 / 状态 / 数据 / 页面 / 组件 / 路由。本页把 wiki 里这条主线上的概念、实体、源摘要拼成一张栈图，给出"什么场景选哪层的哪个工具"的统一视角。

## 为什么需要"栈"这个视角

React 的卖点是渲染原语（component、state、effect），但它**刻意不提供**路由、数据获取、状态管理、项目结构的官方方案。这种极简设计带来两个代价：

1. **小项目爽**——你可以只用 `useState` 完成一个 demo
2. **中大项目乱**——每次迭代都要临时决定"这个状态放哪、这个请求怎么缓存、这个目录放何处"，没有既定框架约束时熵只涨不降

现有的 wiki 页面分别解决其中一层，但孤立看不到全貌——本页把它们组合成一个**栈**，自顶向下是：

```
┌─────────────────────────────────────────┐
│  L0 — 部署与路由                         │  ← SPA fallback / 服务端 rewrite
├─────────────────────────────────────────┤
│  L1 — 项目组织                           │  ← Feature-Based 架构 + 单向依赖
├─────────────────────────────────────────┤
│  L2 — 状态分层                           │  ← 按来源分五类（Component/App/Server/Form/URL）
├─────────────────────────────────────────┤
│  L3 — 数据层（按状态类别选工具）         │  ← TanStack Query / Zustand / RHF / Router
├─────────────────────────────────────────┤
│  L4 — 页面级治理（长期演化的反模式）     │  ← 布尔语义过载 / 内存态单源 / 隐式状态机 ...
├─────────────────────────────────────────┤
│  L5 — 组件级纪律（单组件内部）           │  ← derived state / mutate / index-as-key ...
└─────────────────────────────────────────┘
```

下面逐层解释"问题是什么、工具是什么、常见错误是什么"。

## L0 — 部署与路由

**问题**：SPA 用 History API 做前端路由，刷新 `/foo/bar` 时服务端如果没配 fallback 就 404。看起来不属于"架构栈"，但它是**白屏的第一排雷**。

**工具**：
- 开发：Vite `historyApiFallback` / Webpack dev-server
- 生产：Nginx `try_files $uri /index.html` / CDN 配 200 回 `index.html` / Next.js 自带处理

**关联**：[[wiki/concepts/programming/spa-history-fallback.md|SPA History 路由与服务端 Fallback]]

**常见错误**：本地用 HashRouter 开发 → 上线切 BrowserRouter → 刷新立刻 404。

## L1 — 项目组织（Feature-Based Architecture）

**问题**：按"技术层"（components / hooks / utils / services）组织目录时，单个业务 feature 的代码被切成碎片散在五个目录——改一个功能要跳来跳去。

**工具**：
- 按 **feature 文件夹**自包含（`features/auth/{api,components,hooks,stores}`）
- **单向依赖**：`shared → features → app`，**禁止 features 互相引用**
- 用 ESLint `import/no-restricted-paths` **把架构约束变成可执行规则**（CI 能挂）
- **反 barrel file**（Vite tree-shaking 失效 + 边界隐式化）

**关联**：[[wiki/concepts/programming/feature-based-architecture.md|Feature-Based 架构]] · [[wiki/entities/products/bulletproof-react.md|Bulletproof React]]

**常见错误**：`src/components/` 长成第二个垃圾桶——任何"以后可能用到"的东西都扔进去。解药：**只有真正被 2+ features 引用**才能升到顶层。

## L2 — 状态分层（五分类）

**问题**：把"所有状态都塞 Redux"或"全都用 useState"都是单极化错误。React 应用里的 state 按**值的来源**可以分成五种，每种有各自的生命周期和正确工具。

**五分类**：

| 类别 | 来源 | 默认工具 |
|------|------|---------|
| Component State | 组件私有 | `useState` / `useReducer` |
| Application State | 跨组件客户端 | Zustand / Jotai（小）/ Redux Toolkit（重）/ XState（状态机） |
| Server Cache State | 远端 API | [[wiki/entities/products/tanstack-query.md\|TanStack Query]] / [[wiki/entities/products/swr.md\|SWR]] |
| Form State | 表单字段 | React Hook Form + zod |
| URL State | URL path/query/hash | react-router / Next.js router |

**关联**：[[wiki/concepts/programming/react-state-categories.md|React 状态五分类]]

**判断口诀**：
- 值的权威来源在服务器 → **Server Cache**（即使是"当前登录用户"这种看起来全局的）
- 值应该可分享、可刷新、可收藏 → **URL State**（列表筛选、分页、tab 选中项）
- 值只需组件内部用 → **Component**（从内部起，按需上提）
- 值需跨组件共享但与服务器无关 → **Application**
- 值属于表单字段 → **Form**

## L3 — 数据层（Server Cache 的深水区）

五分类里**唯一配得上一整章的是 Server Cache State**——它有缓存、新鲜度、去重、失效、乐观更新、回滚、分页一整套语义，纯手写能把一个中型项目埋了。

**工具选型**：

| 选 TanStack Query | 选 SWR |
|-------------------|--------|
| 需要明确的 fresh / stale / GC 语义 | 读多写少、轻量场景 |
| 有复杂 mutation（乐观更新、并发控制） | 希望最少抽象 / 小 bundle |
| 想要 DevTools / 持久化 / 无限滚动 | Next.js 内轻量用 |
| 把服务端状态层当团队基础设施 | 复杂度收口到框架层 |

**关联**：[[wiki/concepts/programming/server-state-management.md|服务端状态管理]] · [[wiki/sources/articles/react-query-vs-swr-server-state-source-compare.md|React Query vs SWR 源码对比]]

**常见错误**：
- 把 API 数据放 Zustand / Redux → 重造 react-query 的轮子，而且没它好
- Auth 状态放全局 store → 应该用 `useQuery(['user'])` 管理（`react-query-auth`）
- 列表筛选条件放 `useState` → 应该放 URL（可分享、可刷新）

## L4 — 页面级治理

**问题**：单个页面长期迭代（每次只加一个布尔 / 一个 useEffect / 一个 `??` 兜底）会累积出"300+ 行组件 + 隐式状态机 + 字段级三源拼凑"的坏味道。不立刻出错，但改 bug 危险、加功能慢、边界场景（OAuth 回跳、刷新、整页 redirect）容易白屏。

**四大反模式**：

| 反模式 | 重构对策 |
|-------|---------|
| 布尔语义过载 | 拆成两个独立布尔，职责隔离 |
| 内存态单源 | sessionStorage + `phase` 字段做权威源 |
| 隐式状态机 | 显式 `phase` 枚举 + 单 hook 集中转移 |
| 字段级三源合并 | 单 hook 按源优先级一次决定整对象 |

**关联**：[[wiki/concepts/programming/react-page-state-antipatterns.md|React 页面状态管理反模式]]

**与 L2 的关系**：四反模式本质是"多类 state 被混成一锅"。分清楚 URL / Application / Server Cache 之后，反模式 4 的解法自然出现。

## L5 — 组件级纪律

**问题**：单组件内部（10–50 行）的"一写就错"经典坑。不分 Class 还是 Hooks，语法变了但模型原理不变——**引用比较、快照语义、不可变性**。

**词典**（保留了仍生效的几条）：

| # | 反模式 | 核心原理 |
|---|-------|---------|
| 1 | Props in Initial State | state 初值只算一次，props 后续变化被忽略 |
| 2 | Mutating State | 引用不变 → 浅比较 true → 不重渲染 |
| 3 | Index as Key | key 要绑数据不是绑位置，否则 reconciler 复用错节点 |
| 4 | Spreading Props on DOM | 非 DOM 属性渲染成无效 HTML 属性 |
| 5 | Render 里新建引用 | `React.memo` / `useMemo` 的隐形杀手 |

**关联**：[[wiki/concepts/programming/react-classic-antipatterns.md|React 经典反模式（组件层）]]

**常见错误**：LLM 辅助编码会**放大这些反模式**——默认"照着 props 建 state"、"用 map index 当 key"、"render 里内联 `() => ...`"。给它们起名字之后 review 时能一眼抓出来。

## 层与层之间的冲突与协同

不是每层独立存在——相邻层经常互相倒逼。

**协同**：
- **L1 feature** 内部天然包含 **L2 五分类**：`features/auth/stores` 对应 Application State，`features/auth/api` 对应 Server Cache，`features/auth/components/login-form` 涉及 Form State
- **L3 TanStack Query** 的 `QueryCache` 是全局单例，意味着一个 feature 在任何组件里 `useQuery(['user'])` 都命中同一份缓存——**不用手动抬升到全局 store**，L3 的选对直接化解了 L2 的"要不要放 Zustand"这类误判
- **L4 重构** 的产物（`usePaymentFlow` / `usePaymentContext`）天然落到 **L1 feature 内部**，不会污染 shared 层

**冲突**：
- **L2 vs L3**：Auth 状态看起来是 Application（跨组件共享），实则 Server Cache（权威在服务器）。识别错 → 用错工具 → 重造 react-query 轮子
- **L2 vs L4**：开发初期用 `location.state` 做 Application State 足够（L2 合规），但页面开始 OAuth 重定向后（触发 L4 反模式 2），就得升到 sessionStorage + phase 字段
- **L1 vs L0**：Next.js App Router 把路由和目录绑定，shared `app/` 和 feature 的 `app/` 入口容易打架——**这是 L1 的开放问题**

## 什么时候不需要完整栈

小项目 / demo / 单页工具：
- **跳过 L1**：扁平 `src/` + `pages/` 够用
- **跳过 L3**：直接 `fetch` + `useState` 缓存（数据不复杂的话）
- **保留 L5**：组件级纪律在任何规模都生效

**升级信号**：什么时候从"扁平"长到"全栈"——
- 3+ 工程师并行开发 → 补 L1（feature 隔离）
- 超过 5 个 API endpoint → 补 L3（TanStack Query）
- 某个页面超过 300 行 / 6+ useState → 补 L4（phase 状态机）
- 出现"上线刷新 404" → 补 L0（serve fallback）

## 与其他架构模式的对位

**与后端分层对比**：

| React 栈 | 后端类比 |
|---------|---------|
| L1 Feature-Based | [[wiki/concepts/programming/microservices.md\|微服务架构]]（按业务边界切） |
| L2 状态分层 | [[wiki/concepts/programming/backend-architecture.md\|Clean Architecture]] 的"按来源分层" |
| L3 TanStack Query | 后端的 ORM / Repository + 缓存层 |
| L4 页面重构 | 后端的 service 层重构 |
| L5 组件纪律 | [[wiki/concepts/programming/clean-code.md\|整洁代码]] 的"函数级"建议 |

**共同底层**：[[wiki/concepts/programming/solid-principles.md|SOLID]]（S 单一职责、D 依赖反转）、[[wiki/concepts/programming/clean-code.md|DRY/KISS/YAGNI]]。

## 工具箱一览表

把 wiki 里相关的工具实体按层摆一起：

| 层 | 工具实体 |
|----|---------|
| L0 | （基础设施侧，wiki 暂未建实体页） |
| L1 | [[wiki/entities/products/bulletproof-react.md\|Bulletproof React]]（参考实现） |
| L2 | —（方法论层，非工具） |
| L3 | [[wiki/entities/products/tanstack-query.md\|TanStack Query]] · [[wiki/entities/products/swr.md\|SWR]] |
| L4 | —（重构方法论） |
| L5 | —（纪律层，Immer 可选） |

## 开放问题

- **React 19 + Server Components 会重塑哪些层？** 最直接的影响是 L3——一部分"Server Cache State"可以直接下沉到 Server Components，client bundle 变小。L2 的 Application State 边界也会随之收缩。
- **React Compiler 普及后 L5 的 memo gotcha 还存在吗？** 编译器能自动 memo 化，但目前（2026）覆盖率和稳定性还在爬坡，手写 memoization 仍是兜底。
- **L1 的 feature 何时该升级为 monorepo workspace？** Bulletproof React 不区分，但一旦跨包复用、跨团队所有权出现，`features/` 升级为 `packages/` 更清晰，代价是工具链复杂度。
- **AI 辅助编码如何与这个栈对齐？** LLM 倾向只看眼前代码追加而非重构，L4 和 L5 的反模式会被放大——这让**给反模式起名字**这件事在 AI 时代价值翻倍，review 时能精确指出而不是泛泛说"这里不对"。

## 相关页面

- **L0**：[[wiki/concepts/programming/spa-history-fallback.md|SPA History 路由与服务端 Fallback]]
- **L1**：[[wiki/concepts/programming/feature-based-architecture.md|Feature-Based 架构]]
- **L2**：[[wiki/concepts/programming/react-state-categories.md|React 状态五分类]]
- **L3**：[[wiki/concepts/programming/server-state-management.md|服务端状态管理]]
- **L4**：[[wiki/concepts/programming/react-page-state-antipatterns.md|React 页面状态管理反模式]]
- **L5**：[[wiki/concepts/programming/react-classic-antipatterns.md|React 经典反模式（组件层）]]

## 来源

- [[wiki/sources/articles/bulletproof-react-github.md|Bulletproof React]] — L1 / L2 / L3 的系统化参考
- [[wiki/sources/articles/react-bits-github.md|React Bits]] — L5 的词典
- [[wiki/sources/articles/react-query-vs-swr-server-state-source-compare.md|React Query vs SWR 源码对比]] — L3 的深入
