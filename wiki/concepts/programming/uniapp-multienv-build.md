---
title: uni-app 多端多环境构建
type: concept
subtype: programming
tags: [programming, frontend, build-tools]
created: 2026-04-29
updated: 2026-04-29
sources: []
---

# uni-app 多端多环境构建

> 用一套 Vue 代码构建 H5 / 微信小程序 / 头条小程序，并在多个部署环境（development / test / staging / production）下精确切换 publicPath、appid 等参数的工程方案。

## 问题背景

uni-app 项目的 `manifest.json` 在构建时是静态文件：H5 的 `publicPath`、微信的 `appid`、头条的 `appid` 都写在里面。同一套代码需要支持：

- **3 个平台**：H5 / 微信小程序 / 头条小程序
- **多个环境**：development / test / staging / production
- **每个环境**的 appid 和 CDN publicPath 不同

## 解法：构建前脚本写 manifest

在每条 `package.json` 构建脚本前，先用 Node.js 脚本修改 `manifest.json`，再触发构建：

```json
{
  "scripts": {
    "build:test:h5": "node replaceManifest.js test h5 && cross-env VUE_APP_ENV=test NODE_ENV=production UNI_PLATFORM=h5 vue-cli-service uni-build",
    "build:mp-weixin":  "node replaceManifest.js production mp && cross-env NODE_ENV=production UNI_PLATFORM=mp-weixin vue-cli-service uni-build",
    "build:mp-toutiao": "node replaceManifest.js production dy-mp && cross-env NODE_ENV=production UNI_PLATFORM=mp-toutiao vue-cli-service uni-build"
  }
}
```

### replaceManifest.js 的核心技巧

`manifest.json` 包含 `//` 注释，不能用 `JSON.parse`。解法是**逐行正则替换**：

```js
function replaceManifest(path, value) {
  const arr = path.split('.')          // ['h5', 'publicPath']
  const lines = content.split('\n')
  // 按嵌套层级逐行扫描，找到最深层后，用正则替换该行的值部分
  // 比 JSON.parse 脆弱（依赖格式稳定），但保留了注释
}
```

**改进方向**：用 `json5` 或 `jsonc-parser` 解析带注释的 JSON，保留注释的同时安全写入。

## 三层环境变量分工

不要把三个关注点混用到一个变量里：

| 变量 | 管理什么 | 生效层 | 示例 |
|------|---------|------|------|
| `UNI_PLATFORM` | 编译目标 | 框架层（uni-app）| `h5` / `mp-weixin` / `mp-toutiao` |
| `NODE_ENV` | webpack 模式 | 工程层（webpack）| `development` / `production` |
| `VUE_APP_ENV` | 业务运行时环境 | 代码层（`process.env`）| `test` / `production` |

`VUE_APP_ENV` 可在运行时代码里读取（`process.env.VUE_APP_ENV`），控制 API baseURL 等业务参数。小程序构建时通常不传（小程序没有 H5 的运行时环境区分）。

## publicPath 与 appid 映射规则

### H5 publicPath

| env 参数 | publicPath |
|---------|-----------|
| `development` | `/project-name`（devServer 相对路径）|
| `test` | `https://cdn-test.example.com/project-name` |
| `staging` | `https://cdn.example.com/project-name/build/h5` |
| `production` | `https://cdn.example.com/project-name` |

staging 和 production 的路径差一段 `/build/h5`：production 会在构建后把 `dist/build/h5/` 复制提升到 `dist/`（webpack afterEmit 钩子），staging 不做这步复制。

### 小程序 appid

规则极简：**production 用正式 appid，其余所有环境用测试 appid**。

## 构建后处理：AfterEmitPlugin

在 `vue.config.js` 的 webpack `afterEmit` 钩子里，H5 非开发模式构建完成后额外做：

1. **CSS 缓存破坏**：`index.html` 中的 `.css` 链接追加随机 4 位 `?t=xxxx`
2. **清理 CDN 残留**：删除 CSS 里 uni-app 默认 CDN 域名的 `background-image` 引用
3. **目录对齐**（仅非 staging）：`dist/build/h5/` → 复制到 `dist/`

## 头条小程序的特殊处理

头条小程序需要把支付相关页面外包给字节官方的 `microapp-trade-plugin`（交易插件）。`uniapp-to-group` webpack 插件在构建时自动在 `app.json` 注入三个外部页面：

```js
pages: [
  'ext://microapp-trade-plugin/order-confirm',
  'ext://microapp-trade-plugin/refund-apply',
  'ext://microapp-trade-plugin/refund-detail',
]
```

支付/退款流程走字节官方插件托管，避免自行实现合规性问题。

## 已知痛点

| 痛点 | 现状 | 改进方向 |
|------|------|---------|
| 逐行正则脆弱 | manifest.json 格式变化可能匹配失败 | 改用 json5/jsonc-parser |
| manifest.json git 噪音 | 每次构建都写入，diff 噪音大 | 用模板文件 + .gitignore 忽略生成文件 |
| 头条小程序无 CI | 构建和上传均手动 | 接入 tt-ide-cli 自动上传 |

## 相关概念

- [[config-driven-page|配置驱动落地页]] — 同一仓库的前端动态组装架构
- [[canary-deployment|金丝雀部署]] — 多环境发布的另一种控制策略
