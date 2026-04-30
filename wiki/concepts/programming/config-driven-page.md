---
title: 配置驱动落地页
type: concept
subtype: programming
tags: [programming, architecture, frontend]
created: 2026-04-29
updated: 2026-04-29
sources: []
---

# 配置驱动落地页

> 后端下发渲染配置（组件列表 + 状态），前端按配置动态组装页面，实现"活动内容可变、代码不变"的轻量可配置架构。

## 是什么

配置驱动落地页（Config-Driven Landing Page）是一种前端架构模式，核心思路：

```
后端 API 返回：
  componentList: [
    { name: 'kit-image-home',  state: { imageUrl: '...' } },
    { name: 'kit-button-price', state: { price: 99, btnText: '立即购买' } },
    ...
  ]

前端按 name 查找对应组件，按 state 传 props 渲染：
  v-for componentList
    → getVM(kit.name) → <KitComponent v-bind="kit.state" />
```

运营/产品通过后台系统修改配置，**无需发版**即可改变落地页内容。

## 核心要素

### 1. 标准化组件单元（Kit）

每个 Kit = 元数据（`config.json`）+ 渲染组件（`view.vue`）：

```json
// config.json
{
  "name": "kit-button-price",   // 唯一标识，与后端配置中的 name 对应
  "cnName": "价格按钮",
  "category": "purchase-button",
  "condition": { "max": "1", "fixed": "bottom" }
}
```

- `name`：前后端对齐的 key，**必须稳定**，一旦上线不能随意改名
- `condition`：编辑态约束（最多几个、布局约束），C 端渲染不依赖
- `view.vue`：只负责渲染 `state` 里的字段，不直接调用业务 API

### 2. 批量自动注册（require.context）

用 webpack 的 `require.context` 扫描组件目录，免去手动维护注册表：

```js
// 扫描所有 config.json 和 view.vue
const configs = require.context('./kitTemplate', true, /config\.json$/)
const views   = require.context('./kitTemplate', true, /view\.vue$/)

// 用目录名（folderKey）对齐 config 与 view
const vm = views.find(v => v.folderKey === conf.folderKey)
```

**新增组件只需建目录**，不改注册代码。

### 3. 后端下发渲染列表

接口返回 `[{ name, state }]`，前端按 `name` 取组件、按 `state` 传 props：

```html
<component
  v-for="kit in renderList"
  :is="getVM(kit.name)"
  v-bind="kit.state"
/>
```

### 4. 编辑态 / 渲染态分离

同一个 `view.vue` 通过 `preview: Boolean` prop 区分两种状态：
- `preview=true`：后台编辑器预览（只读，无交互）
- `preview=false`：C 端生产渲染（完整交互）

## 与低代码平台的区别

| 维度 | 配置驱动落地页 | 低代码平台 |
|------|-------------|---------|
| 编辑器 | 后台系统（另行建设）| 内置可视化拖拽编辑器 |
| 组件来源 | 前端研发维护 Kit | 平台提供通用组件 + 自定义扩展 |
| 灵活性 | 受限于 Kit 池 | 更高，可任意组合 |
| 接入成本 | 低（只要有组件池和接口协议）| 高（需接入平台 SDK）|
| 适合团队 | 有固定组件池的业务线 | 需要快速搭建多样页面的运营团队 |

## 已知权衡与局限

| 权衡点 | 现状 | 改进方向 |
|--------|------|---------|
| Bundle 体积 | require.context 把所有组件全打进主包（34个 Kit 全量）| 按需懒加载（dynamic import + 路由懒加载）|
| 分发器硬编码 | `_element.vue` 对每个 Kit name 写一个 `v-if` 分支 | 用 `<component :is="getVM(name)">` 动态组件替代 |
| Kit name 重命名风险 | name 是前后端协议的 key，改名需双方同步发布 | 用版本字段做兼容，或建立 name alias 机制 |

## 适用场景

- 高频发布的电商活动/营销落地页（每次活动只改内容）
- 多活动页结构相似但内容不同，希望复用组件池
- 前后端分离架构，后端控制"放什么组件"，前端控制"组件长什么样"
- 团队有独立的后台配置系统（或愿意建设一个）

## 实战案例

- **ada-sale-activity**：34 个 Kit，kitController/client.js 注册，detail.vue 消费，支持 H5 + 微信小程序 + 头条小程序三端

## 相关概念

- [[design-patterns|设计模式]] — Strategy 模式（按 name 分发）、Template Method（preview prop）
- [[feature-based-architecture|Feature-Based Architecture]] — 按功能而非类型组织组件目录的相关实践
- [[uniapp-multienv-build|uni-app 多端多环境构建]] — 同一套代码在多端部署的构建机制
