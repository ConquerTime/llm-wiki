---
title: Bulletproof React — 生产级 React 架构指南
type: source
subtype: article
tags: [programming, react, architecture, best-practice]
created: 2026-04-27
updated: 2026-04-27
author: Alan Alickovic
url: https://github.com/alan2207/bulletproof-react
date: 2026-04
sources:
  - "[[raw/articles/bulletproof-react/README.md|Bulletproof React README]]"
  - "[[raw/articles/bulletproof-react/project-structure.md|Project Structure]]"
  - "[[raw/articles/bulletproof-react/state-management.md|State Management]]"
  - "[[raw/articles/bulletproof-react/components-and-styling.md|Components and Styling]]"
  - "[[raw/articles/bulletproof-react/api-layer.md|API Layer]]"
  - "[[raw/articles/bulletproof-react/project-standards.md|Project Standards]]"
  - "[[raw/articles/bulletproof-react/error-handling.md|Error Handling]]"
  - "[[raw/articles/bulletproof-react/performance.md|Performance]]"
  - "[[raw/articles/bulletproof-react/testing.md|Testing]]"
  - "[[raw/articles/bulletproof-react/security.md|Security]]"
---

# Bulletproof React — 生产级 React 架构指南

> 一份由 [[alan-alickovic|Alan Alickovic]] 维护的意见性 React 架构指南（GitHub 35k+ 星），通过 **feature-based 项目结构 + 单向架构约束 + 状态五分类**，给出从新项目启动到大规模团队协作的一整套最佳实践。

## 核心论点

1. **React 的自由度是双刃剑**——没有预定义架构容易产出混乱、不一致、过度复杂的代码库；bulletproof-react 提出一套"够好即可"的默认方案，重点不是模板而是原则。
2. **以 feature 组织代码**——把大部分代码放 `src/features/<name>/{api,components,hooks,stores,types,utils}`，禁止跨 feature 直接引用，feature 只能在 app 层组合。
3. **强制单向依赖**（unidirectional codebase）——`shared → features → app`，用 ESLint 的 `import/no-restricted-paths` 在构建时把架构约束变成可执行规则。
4. **状态要按来源分五类**——Component / Application / Server Cache / Form / URL，不同类别用不同工具（useState, zustand, react-query, react-hook-form, react-router），避免"所有东西塞 Redux"。
5. **就近原则（colocation）** 贯穿组件、样式、状态——状态从组件内部起，按需上提，不预先全局化。
6. **测试倒金字塔**——集成测试优先，单元测试只测真正独立的部分，E2E 兜底。
7. **安全默认值**——认证 token 走 `HttpOnly` Cookie 而非 localStorage；错误边界多处而非单一；错误通过拦截器统一处理。

## 关键摘录

### 项目结构（来自 [[raw/articles/bulletproof-react/project-structure.md|Project Structure]]）

> For easy scalability and maintenance, organize most of the code within the features folder. Each feature folder should contain code specific to that feature, keeping things neatly separated.

> It might not be a good idea to import across the features. Instead, compose different features at the application level.

单向架构通过 ESLint 强制：

```js
'import/no-restricted-paths': [
  'error',
  {
    zones: [
      // features 不能反向引用 app
      { target: './src/features', from: './src/app' },
      // shared 模块不能引用 features 或 app
      {
        target: ['./src/components', './src/hooks', './src/lib', './src/types', './src/utils'],
        from:   ['./src/features', './src/app'],
      },
    ],
  },
],
```

> In the past, it was recommended to use barrel files to export all the files from a feature. However, it can cause issues for Vite to do tree shaking and can lead to performance issues. Therefore, it is recommended to import the files directly.

值得注意：作者**反对 barrel file**，与多数 React 样板的建议相反。

### 状态五分类（来自 [[raw/articles/bulletproof-react/state-management.md|State Management]]）

| 分类 | 工具建议 |
|------|---------|
| **Component State** — 组件私有 | `useState` / `useReducer` |
| **Application State** — 跨组件全局 | Context+hooks / Redux Toolkit / Zustand / Jotai / XState |
| **Server Cache State** — 来自 API 的远端数据 | [[products/tanstack-query\|React Query]] / [[products/swr\|SWR]] / Apollo / urql / RTK Query |
| **Form State** — 表单字段 | React Hook Form / Formik / Final Form，配合 zod/yup 校验 |
| **URL State** — URL 参数/查询串 | react-router-dom |

关键原则：

> Avoid unnecessarily globalizing all state variables from the outset to maintain a structured and efficient state management architecture.

> The Server Cache State refers to the data retrieved from the server that is stored locally on the client-side for future use. While it is feasible to cache remote data within a state management store like Redux, there exist more optimal solutions to this practice.

### API 层（来自 [[raw/articles/bulletproof-react/api-layer.md|API Layer]]）

每个 API 请求的三件套：

- Types 和 validation schemas（请求+响应）
- fetcher function（调用预配置的单一 API client 实例）
- hook（基于 react-query / swr 管理缓存）

### 性能优化（来自 [[raw/articles/bulletproof-react/performance.md|Performance]]）

> The `children` prop is the most basic and easiest way to optimize your components. When applied properly, it eliminates a lot of unnecessary rerenders.

```javascript
// 未优化：PureComponent 会随 Counter 内 count 更新重渲染
const Counter = () => {
  const [count, setCount] = useState(0);
  return <div>...<PureComponent /></div>;
};

// 优化：children 由父级传入，Counter state 更新不影响它
const Counter = ({ children }) => {
  const [count, setCount] = useState(0);
  return <div>...{children}</div>;
};
```

状态初始化的惰性函数：

```javascript
// 每次重渲染都会运行 myExpensiveFn
const [state, setState] = useState(myExpensiveFn());
// 只运行一次
const [state, setState] = useState(() => myExpensiveFn());
```

作者也警告 Context 被过度使用：

> Do not rush with context and global state. Context is often used as the "golden tool" for props drilling, whereas in many scenarios you may satisfy your needs by lifting the state up or a proper composition of components.

### 安全（来自 [[raw/articles/bulletproof-react/security.md|Security]]）

> Storing authentication tokens in localStorage can pose a security risk, especially in the context of Cross-Site Scripting (XSS) vulnerabilities. Opting to store tokens in cookies, configured with the `HttpOnly` attribute, can enhance security as they are inaccessible to client-side JavaScript.

授权模型推荐 RBAC + PBAC 混用：RBAC 做粗粒度角色门槛，PBAC 做细粒度所有权检查（如"只有评论作者能删除自己的评论"）。

### 错误处理（来自 [[raw/articles/bulletproof-react/error-handling.md|Error Handling]]）

> Instead of having only one error boundary for the entire app, consider placing multiple error boundaries in different areas. This way, if an error occurs, it can be contained and managed locally without disrupting the entire application's functionality.

### 测试（来自 [[raw/articles/bulletproof-react/testing.md|Testing]]）

> The efficacy of testing lies in the comprehensive coverage provided by integration and e2e tests.

推荐工具链：Vitest + Testing Library + Playwright + MSW。MSW 在开发和测试中复用同一套 mock handler，避免维护两套。

## 项目规模

仓库包含三个对等示例应用：
- `apps/react-vite/` — Vite + React
- `apps/nextjs-app/` — Next.js App Router
- `apps/nextjs-pages/` — Next.js Pages Router

展示同一套架构原则在不同 meta-framework 下的落地。

## 提到的实体

- [[alan-alickovic|Alan Alickovic]] — 作者
- [[bulletproof-react|Bulletproof React]] — 项目本身

## 提到的概念

- [[feature-based-architecture|Feature-Based 架构]] — 本文的核心组织原则
- [[react-state-categories|React 状态五分类]] — 本文"State Management"小节的提炼
- [[server-state-management|服务端状态管理]] — 本文"Server Cache State"小节
- [[react-page-state-antipatterns|React 页面状态管理反模式]] — 状态五分类是其上位框架
- [[clean-code|整洁代码]] / [[refactoring|重构]] / [[solid-principles|SOLID 原则]] — 通用原则的 React 落地

## 提到的工具

- [[products/tanstack-query|TanStack Query]] / [[products/swr|SWR]] — Server Cache 层
- Zustand / Jotai / Redux Toolkit / XState — Application State 层
- React Hook Form / zod — 表单 + 校验
- Vitest / Testing Library / Playwright / MSW — 测试工具链
- ESLint / Prettier / Husky / TypeScript — 项目标准工具
- Sentry — 生产错误追踪
