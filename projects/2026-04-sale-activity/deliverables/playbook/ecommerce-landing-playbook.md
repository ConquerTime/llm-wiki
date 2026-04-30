# 电商活动落地页开发规范

> 从 ada-sale-activity 实战提炼的**最佳实践**与**反模式**，脱离该仓库后仍然成立。

---

## 1. 架构层：先定分层，再写代码

### ✅ 实践：三层职责分离

| 层次 | 职责 | ada-sale-activity 对应 |
|------|------|----------------------|
| **页面层** | 编排 Kit 列表，持有页面级状态（pageInfo, products） | `detail.vue` + `StoreOrderMixin` |
| **组件层** | 单一 UI 模块，只关心渲染自己的 `state` | 各 `kitTemplate/*/view.vue` |
| **逻辑层** | 下单/支付/登录等跨组件流程，以 mixin/composable 封装 | `order.ts`, `pay.ts`, `checkLogin.ts` |

**检查点**：如果页面组件超过 200 行，或者一个 mixin 超过 500 行，考虑是否职责已经越界。

### ⚠️ 反模式：把业务逻辑写进 Kit 组件

Kit 的 `view.vue` 应该只管渲染，不应该直接 import API 或触发下单流程。正确做法：Kit 向外 `$emit`，由页面层的 mixin 处理。

---

## 2. 构建层：一套代码，多端多环境

### ✅ 实践：replaceManifest 前置脚本模式

适用于任何 uni-app 多端多环境项目：

```
package.json scripts:
  "build:test:h5": "node replaceManifest.js test h5 && cross-env ... vue-cli-service uni-build"
```

**三个环境变量各司其职**（不要混用）：

| 变量 | 管理什么 | 生效层 |
|------|---------|------|
| `UNI_PLATFORM` | 编译目标（h5/mp-weixin/mp-toutiao） | 框架层 |
| `NODE_ENV` | webpack 模式（development/production） | 工程层 |
| `VUE_APP_ENV` | 业务运行时环境（test/production） | 代码层 |

### ✅ 实践：AfterEmitPlugin 的 CSS 缓存破坏

生产 H5 构建完成后，在 webpack `afterEmit` 钩子里对 index.html 中的 `.css` 引用追加 `?t=随机4位`。比 webpack 的 contenthash 更简单，且对 CDN 强缓存配置兼容性好。

### ⚠️ 反模式：逐行正则解析带注释的 JSON

`manifest.json` 含 `//` 注释，不能 `JSON.parse`，于是用逐行正则替换。这种做法脆弱：一旦字段格式换行方式改变就可能匹配失败。**改进方向**：用 `json5` 或 `jsonc-parser` 解析，保留注释的同时安全写入。

### ⚠️ 反模式：manifest.json 频繁被 git 追踪

每次构建都写入 manifest.json，导致 git 历史里 diff 噪音大（ada 仓库第 3 热文件，28 次提交）。**改进方向**：用 `manifest.template.json` + `.gitignore` 忽略生成文件。

---

## 3. 发布层：CI/CD 流水线设计

### ✅ 实践：feature → master → online 三段式分支

| 分支 | 职责 | 触发 CI |
|------|------|--------|
| `feature-*` | 功能开发 | 无 |
| `master` | 测试主干 | 构建测试包 + 小程序上传 |
| `online` | 正式发布 | 构建 + OSS 发布 |

适合**发布节奏明确**的项目。缺点：两条主干维护成本；cherry-pick 或 merge 时需要额外操作。

### ✅ 实践：miniprogram-ci 自动注入 git 信息

上传微信小程序时，`desc` 字段自动读 git 信息，不用手动填备注：

```js
desc: `【${currentBranch}】（${latestAuthor}）${latestLog}`
// 上传后在微信开发者平台可直接追踪来源
```

**可直接复用到任何微信小程序 CI 脚本**。

### ⚠️ 反模式：正式小程序手动发布

ada-sale-activity 只有 `test-mp-build-job`（测试小程序 CI 上传），正式小程序没有自动化。每次正式发布靠手动执行 `build:mp-weixin + upload`，是已知流程缺口。

**修复方案**：在 `online` 分支 stage 里加一个 `online-mp-build-job`，仿照测试 stage 结构，用 `production` appid 构建并上传。

### ⚠️ 反模式：版本号硬编码

`npm run upload -- --version=1.0.0` 永远上传 1.0.0，在微信平台无法区分版本。**改进**：从 `package.json version` 或 `git tag` 自动读取。

---

## 4. 下单支付层：最复杂链路的管理方法

### ✅ 实践："校验链"模式

多步骤表单提交的通用结构：

```
入口方法
  → 前置校验（SKU → 学员信息 → 家长锁 → 防重复提交）
    → 核心业务（createOrder → handlePay）
      → 错误处理（按 HTTP status 枚举，fallback → Sentry）
```

每个校验步骤失败时**直接 return**，不嵌套 if-else，保持线性可读。

### ✅ 实践：广告回传与业务逻辑分离

分两个时间点上报，互不阻塞：

```
payClickAdsReport()    ← 用户点击时（无需登录）
payVerifiedAdsReport() ← 已完成登录后
```

两个上报都用 `.catch` 静默处理，**不允许广告上报失败导致主流程中断**。

### ✅ 实践："支付路由器"模式

一个统一的 `pay(data, payType, bizType, options)` 函数，内部按 `payType` 分发到各平台实现。调用方无需感知底层差异：

```
pay(...)
  ├── zeroPay → zeroPay()
  ├── wxpay   → wechatPay()
  ├── alipay  → aliPay()
  └── iap     → iosIAPPay()
```

适合所有需要支持多种支付方式的场景。

### ✅ 实践：customCreateOrder() 钩子——模板方法扩展

在 `BaseOrderMixin.createOrder()` 执行前调用 `customCreateOrder()`，返回 `true` 则跳过标准逻辑：

```ts
customCreateOrder(): boolean {
  this.createSpecialOrder()
  return true  // 阻止标准 createOrder 执行
}
```

**这是唯一正确的扩展方式**。直接覆盖 `createOrder()` 会导致校验链断裂。

### ⚠️ 反模式：限流重试用实例变量计数

```ts
retryTime = 0  // 实例变量
onError("活动火爆"): retryTime += 1; if (retryTime > 3) 停止; else createOrder()
```

并发情况下 `retryTime` 可能被多个调用共享导致失控。**改进**：用闭包或独立 retry 工具函数，附带 exponential backoff。

### ⚠️ 反模式：单文件承载全部下单逻辑

`order.ts` 1643 行，价格计算 + 广告回传 + 支付后处理 + 错误处理全部耦合在一个文件里，1548 次提交中有 53 次集中于此。

**拆分方向**：
- `useDiscount.ts` — 价格计算（salePrice / finalPrice / coupon / coin / beanVoucher）
- `useAdsReport.ts` — 广告回传（payClickAdsReport / payVerifiedAdsReport / getReportParams）
- `usePayResult.ts` — 支付后处理（polling / ABTest / result page routing）
- `useOrderValidation.ts` — 校验链（SKU / 学员信息 / 家长锁 / 隐私协议）

---

## 5. Kit 组件层：配置驱动落地页

### ✅ 实践：标准化 Kit 单元

每个 Kit = `config.json`（元数据）+ `view.vue`（渲染）。

**config.json 的 `condition` 字段只在编辑态生效**，C 端渲染直接使用后端下发的已校验配置，不需要前端重复校验。

### ✅ 实践：require.context 批量自动注册

新增 Kit 只需在 `kitTemplate/` 下建目录，不改任何注册代码。`folderKey`（目录名前缀）作为 config.json 与 view.vue 的对齐 key：

```js
const vm = templates.find(it => it.folderKey === conf.folderKey)
```

**代价**：所有 34 个 Kit 在构建时全部打进 bundle（无懒加载），bundle 体积随 Kit 数量线性增长。

### ✅ 实践：`preview` prop 区分预览态和生产态

所有 Kit view.vue 都接受 `preview: Boolean`，同一组件可在后台预览和 C 端复用，不用维护两套组件。

### ⚠️ 反模式：_element.vue 硬写 v-if 分发

当前实现对每个 Kit name 手写一个 `v-if` 分支，新增 Kit 需要改 `_element.vue`，与"注册自动化"理念矛盾。

**更好的实现**：
```html
<!-- 用动态组件代替一长串 v-if -->
<component :is="kitClient.getVM(kit.name)" v-bind="kit.state" />
```

---

## 6. 跨层通用原则

### 环境差异隔离原则
所有"环境判断"（env 值比较、appid 切换、CDN 域名）集中到配置层（`replaceManifest.js` / `pay.ts` 的路由表），业务逻辑代码不直接出现 `if (env === 'xxx')` 散弹。

### 失败不阻塞主流程原则
所有"非核心"操作（广告上报、Sentry、埋点）必须有 `.catch` 静默处理，不允许这些操作的异常冒泡到主链路。

### 扩展点显式声明原则
可被子类/调用方定制的行为应该显式声明为钩子（如 `customCreateOrder()`），而不是隐式依赖 mixin 覆盖或 prototype 改写。这样在 code review 时可以直接找到所有扩展点。
