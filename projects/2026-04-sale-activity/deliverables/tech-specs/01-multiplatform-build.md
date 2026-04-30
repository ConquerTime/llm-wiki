# 技术方案 #1：多端构建与 manifest 替换机制

> ada-sale-activity 如何用一套代码构建 H5 / 微信小程序 / 头条小程序，并在三端 × 五环境下精确切换 publicPath / appid。

---

## 1. 问题背景

uni-app 项目的 `src/manifest.json` 在构建时是**静态文件**：H5 的 `publicPath`、微信的 `appid`、头条的 `appid` 都写死在里面。如果不处理，同一套代码只能构建一个环境。

该项目需要支持：

- **3 个平台**：H5、微信小程序（mp-weixin）、头条小程序（mp-toutiao）
- **5 个环境**：development / test / staging-test / staging / production
- **2 组 appid**：每个小程序平台各有测试/正式两个 appid

解法：**构建前用 Node.js 脚本动态修改 manifest.json，再触发 uni-app 构建**。

---

## 2. 解法：replaceManifest.js

### 2.1 核心逻辑

```
node replaceManifest.js <env> <platform>
     └── 读 manifest.json（字符串）
     └── 按 env 决定 publicPath / appid 的目标值
     └── 用逐行正则替换写入目标字段
     └── 覆写 manifest.json
     └── 触发后续的 vue-cli-service uni-build
```

`replaceManifest` 函数用路径表达式（`"h5.publicPath"`）定位 JSON 字段，**逐行扫描**而非解析 JSON，避免了注释被 JSON.parse 吞掉的问题（manifest.json 含 // 注释，标准 JSON 不允许）：

```js
function replaceManifest(path, value) {
  const arr = path.split('.')          // ['h5', 'publicPath']
  // 逐行扫描，按嵌套顺序匹配每一层 key
  // 找到最深层时，用正则替换该行的值部分
}
```

### 2.2 环境 → publicPath 映射（H5）

| env | publicPath |
|-----|-----------|
| development | `/ada-sale-activity`（本地 devServer 相对路径）|
| test | `https://static-nginx-test.fbcontent.cn/ada-sale-activity` |
| staging-test | `https://static-nginx-test.fbcontent.cn/ada-sale-activity/build/h5` |
| staging | `https://static-common.fbcontent.cn/ada-sale-activity/build/h5` |
| production | `https://static-common.fbcontent.cn/ada-sale-activity` |

staging 和 production 的 publicPath 差一段 `/build/h5`，因为 staging 产物不做 `dist/build/h5 → dist/` 复制（`vue.config.js` 的 `AfterEmitPlugin` 里有判断 `BUILD_ENV === 'staging'` 则 return）。

### 2.3 环境 → appid 映射（小程序）

| platform | env=production | env≠production |
|----------|---------------|---------------|
| mp-weixin | `wxaffa2c82823c1b0f` | `wx151572c499e056c2` |
| mp-toutiao | `tt551f23a2ca20ce4b01` | `ttedec9b5172d372a201` |

规则简单：**production 用正式 appid，其余所有环境用测试 appid**。

---

## 3. npm scripts 全矩阵

`package.json` 14 条构建脚本，规律清晰：

```
node replaceManifest.js <env> <platform>  &&  cross-env <ENV_VARS>  vue-cli-service uni-build [--watch]
```

| script | env | platform | 用途 |
|--------|-----|---------|------|
| `dev:h5` | development | h5 | 本地开发，HMR |
| `dev:mp-weixin` | development | mp | 本地开发，--watch |
| `dev:mp-toutiao` | development | dy-mp | 本地开发，--watch |
| `build:test:h5` | test | h5 | 测试环境 H5 构建 |
| `build:test:staging:h5` | staging-test | h5 | staging 测试版 H5 |
| `build:test:mp-weixin` | test | mp | 测试环境微信，--minimize |
| `build:test:mp-toutiao` | test | dy-mp | 测试环境头条 |
| `build:h5` | production | h5 | 正式 H5 |
| `build:staging:h5` | staging | h5 | staging 正式 H5 |
| `build:mp-weixin` | production | mp | 正式微信小程序 |
| `build:mp-toutiao` | production | dy-mp | 正式头条小程序 |

关键环境变量：
- `UNI_PLATFORM`：告诉 uni-app 编译目标（h5 / mp-weixin / mp-toutiao）
- `VUE_APP_ENV`：运行时可读的业务环境变量（test / production），小程序构建时不传
- `NODE_ENV`：webpack mode（development / production），影响压缩和 sourcemap
- `BUILD_ENV`：仅 staging 时为 `staging`，控制 AfterEmitPlugin 的复制行为

---

## 4. 构建后处理：AfterEmitPlugin（vue.config.js）

H5 非开发模式构建完成后，webpack `afterEmit` 钩子额外做三件事：

```
1. CSS 缓存破坏：index.html 里的 .css 链接追加随机 4 位 ?t=xxxx
2. 清理 uni-app CDN 残留：删除 CSS 文件里 dcloud.net.cn 域名的 background-image 引用
3. 目录对齐（仅非 staging）：
   dist/build/h5/ → 复制到 dist/
   （让 CI 发布 dist/ 时能直接拿到 H5 产物，不用指定子路径）
```

staging 跳过第 3 步，因为 staging 的 OSS 路径就是 `.../build/h5/`，不需要提升。

---

## 5. 头条小程序的特殊处理：uniapp-to-group

头条小程序需要将支付相关页面外包给字节官方的 `microapp-trade-plugin`（交易插件）。`uniapp-to-group` 这个 webpack 插件在构建时把 `package.json` 写入产物，并在 `app.json` 里注入三个外部页面：

```js
pages: [
  'ext://microapp-trade-plugin/order-confirm',  // 提单页
  'ext://microapp-trade-plugin/refund-apply',   // 退款申请页
  'ext://microapp-trade-plugin/refund-detail',  // 退款详情页
]
```

这意味着头条小程序的支付/退款流程**不在本仓库实现**，而是走字节官方插件托管，避免了自行实现合规性问题。

---

## 6. 已知痛点 / 可改进点

| 痛点 | 现状 | 改进方向 |
|------|------|---------|
| replaceManifest 逐行正则脆弱 | 若 manifest.json 格式变化（字段换行方式）可能匹配失败 | 改用 JSON5/JSONC 解析库，保留注释的同时安全写入 |
| staging/production publicPath 路径差异 | 靠 AfterEmitPlugin 的目录复制对齐，逻辑隐蔽 | 统一 OSS 路径，消除 build/h5 的差异层 |
| 头条小程序无 CI 自动上传 | saber.yml 没有头条的 upload stage | 接入头条 CI 工具（tt-ide-cli 或官方 API） |
| manifest.json 频繁被脚本写入 | git 历史里第 3 热的文件（28次），diff 噪音大 | 把 manifest.json 加入 .gitignore，改用模板 + 生成 |

---

## 7. 可复用的设计模式

> 以下内容脱离 ada-sale-activity 后仍然成立，适合回流到 wiki。

**"构建前脚本写 manifest"模式**适用于任何 uni-app 多端多环境项目：
- 在 `package.json scripts` 里，每条构建命令前缀 `node replaceManifest.js <env> <platform> &&`
- replaceManifest.js 只做一件事：按参数写入 manifest.json 的对应字段
- 优点：manifest.json 可以提交到 git（保存默认值），脚本幂等可重复执行
- 缺点：逐行正则替换，对 JSON 格式有隐含假设，建议改用 JSONC 解析

**环境变量分工**（三个变量各司其职）：
- `UNI_PLATFORM`：编译目标（框架层）
- `NODE_ENV`：webpack 模式（工程层）
- `VUE_APP_ENV`：业务环境（运行时层，`process.env.VUE_APP_ENV` 可在代码里读取）
