---
title: Feature-Based 架构
type: concept
subtype: programming
tags: [programming, react, architecture]
created: 2026-04-27
updated: 2026-04-27
sources:
  - "[[wiki/sources/articles/bulletproof-react-github.md|Bulletproof React]]"
---

# Feature-Based 架构

> 按**业务特性（feature）**而非技术职责（components/hooks/utils）来组织代码，每个 feature 自成闭环；配合**单向依赖约束**（shared → features → app），让中大型前端应用随规模增长依然可读、可拆。

## 是什么

传统 React 项目常按"技术层"划分目录：

```
src/
  components/
  hooks/
  utils/
  pages/
  services/
```

随着应用增长，业务代码被切碎散布在多个目录里——改一个 feature 要跳 5 个目录，component 和它的 hook 在物理上相距甚远。

Feature-based 架构把这层翻转过来：

```
src/
  app/          # 路由、provider、应用装配
  features/
    auth/
      api/
      components/
      hooks/
      stores/
      types/
      utils/
    discussions/
      ...
  components/   # 真正跨 feature 共享的 UI
  hooks/        # 真正跨 feature 共享的 hooks
  lib/          # 三方库封装
```

**核心规则**：
1. **大部分代码住在 `features/` 下**——每个 feature 是一个小的自包含模块
2. **禁止跨 feature 直接引用**——`features/auth` 不能从 `features/comments` 引 import
3. **只能在 app 层组合 features**——路由页面是 features 的组装点
4. **单向依赖**：`shared → features → app`（shared 模块不能反向引用 features / app）

## 为什么重要

### 解决"业务代码被技术目录打散"
找一个功能的代码不用跨越多个目录。新加 feature 就是新建一个自闭合文件夹，删 feature 就是删一个文件夹。

### 让架构约束可执行
单向依赖不是口号，可以用 ESLint 的 `import/no-restricted-paths` 在构建期强制：

```js
'import/no-restricted-paths': ['error', {
  zones: [
    // 禁止 features 互相引用
    { target: './src/features/auth',    from: './src/features', except: ['./auth'] },
    { target: './src/features/comments', from: './src/features', except: ['./comments'] },

    // 单向：features 不能反向引 app
    { target: './src/features', from: './src/app' },

    // 单向：shared 模块不能引 features / app
    {
      target: ['./src/components', './src/hooks', './src/lib', './src/types', './src/utils'],
      from:   ['./src/features', './src/app'],
    },
  ],
}]
```

当一条 import 违反了架构约定，CI 直接挂掉——不用靠 code review 捕捉。

### 降低团队协作冲突
不同 feature 文件夹不重叠，多个工程师并行开发时 merge 冲突天然减少。

### 利于重构和迁移
跨 meta-framework 迁移（Vite → Next.js App Router → Next.js Pages）时，`features/` 几乎可以原样搬走——变的只是 `app/` 这个装配层。

## 关键特征

### feature 文件夹的内部结构
```
features/awesome-feature/
  api/        # 该 feature 的 API 请求声明 + hooks
  components/ # 仅该 feature 使用的组件
  hooks/      # 仅该 feature 使用的 hooks
  stores/     # 该 feature 的本地 state stores
  types/      # 仅该 feature 的类型定义
  utils/      # 仅该 feature 的工具函数
  assets/     # 该 feature 专用的静态资源
```

**原则**：只包含这个 feature 用到的东西。如果某段代码被 2+ features 用，就上移到顶层 `components/` / `hooks/` / `lib/`。

### 什么该放 `features/`，什么该放顶层

| 特征 | 位置 |
|------|------|
| 跨 feature 复用的 Button、Modal、Input | `src/components/` |
| 跨 feature 复用的 `useDebounce`、`useMediaQuery` | `src/hooks/` |
| 配置好的 axios client、日期库封装 | `src/lib/` |
| "只有 auth 需要的"登录表单 | `features/auth/components/` |
| "只有 discussions 需要的"讨论列表 hook | `features/discussions/hooks/` |

判断标准：**这段代码只服务一个 feature 吗？**是 → `features/<name>/`；否 → 顶层。

### 反对 barrel file

Bulletproof React 的一个反直觉建议：**不要用 `index.ts` barrel file 重新导出 feature 内容**。

原因：
- Vite 的 tree-shaking 在 barrel 下失效，dev server 冷启动变慢
- barrel 让 feature 的"对外 API"隐式化，反而鼓励外部越界 import

替代：直接从具体文件 import，配合绝对路径（`@/features/auth/components/login-form`）保持可读性。

## 常见误区

### 误区 1：把 feature 当"文件夹"而非"模块"
feature 的本质是"对外暴露的 API 边界"，不是"一堆文件的集合"。判断一个 feature 拆得是否合理：**能否独立讲清它做什么、它依赖哪些 shared、它如何被 app 使用**。

### 误区 2：feature 之间偷偷互相引用
当 `features/comments` 需要 `features/auth` 的东西时，正确做法不是直接 import，而是：
- 该共享的东西上移到顶层（比如 `auth` context、`useUser` hook 移到 `src/lib/auth.tsx`）
- 在 app 层把两个 feature 组合（通过 props 或上下文传递）

### 误区 3：shared 层长成另一个巨石
`src/components/`、`src/lib/` 容易变成第二个"所有东西都往这塞"的垃圾桶。解药：**只有真正被 2+ features 使用的东西才能进 shared**。"可能以后会用到"不算。

### 误区 4：把所有 API 调用放 feature 内
有时候多个 feature 共享同一组 API 端点，这时可以在顶层 `src/api/` 集中声明，避免 feature 间的隐式耦合。

## 与相关模式的关系

- [[clean-code|整洁代码]] 的模块化原则在前端的具体落地
- [[solid-principles|SOLID 原则]] 中 "S"（单一职责）在目录组织层面的体现
- 与 [[microservices|微服务架构]] 在思想上同构——都是"按业务边界切分，强制依赖方向"
- 与 [[react-page-state-antipatterns|React 页面状态反模式]] 互补——feature 内部的状态组织问题由状态五分类框架解决，feature 之间的组织问题由本架构解决

## 开放问题

- **monorepo 里 feature 是否该进一步升为独立 package？** bulletproof-react 本身不区分，但规模再大时把 feature 升级为 workspace package（各自 `package.json`）能强化边界；代价是工具链复杂度。
- **Next.js App Router 下 `app/` 和 `features/` 的边界如何定？** App Router 的文件即路由天然占用 `app/`，features 仍可独立存在，但路由层和 feature 的"入口组件"之间容易出现薄层重复。
- **feature 大到什么程度该拆？** 经验规则：一个 feature 超过 15-20 个文件 / 超过 2 个工程师日常维护时，考虑拆成 sub-features。

## 相关概念

- [[react-page-state-antipatterns|React 页面状态管理反模式]] — feature 内部的状态组织问题
- [[server-state-management|服务端状态管理]] — feature 内 `api/` 目录的职责范围
- [[clean-code|整洁代码]] / [[refactoring|重构]] / [[solid-principles|SOLID 原则]] — 上位原则

## 来源

- [[wiki/sources/articles/bulletproof-react-github.md|Bulletproof React]]
