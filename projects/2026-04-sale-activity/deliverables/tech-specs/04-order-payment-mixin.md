# 技术方案 #4：下单与支付 Mixin 体系

> ada-sale-activity 如何用 Vue 2 Mixin 分层管理"点击购买 → 校验 → 下单 → 支付 → 结果页"的完整链路，以及多端/多 App/多支付方式的分发机制。

---

## 1. 问题背景

电商落地页的"下单 → 支付"链路是整个系统中**最复杂的部分**：

- **多端差异**：H5 微信内 / H5 微信外 / H5 App 内 / 微信小程序 / 头条小程序，每端的支付 API 不同
- **多 App 差异**：猿编程（ybc）/ 辅导（fudao）/ 斑马（zebra）/ 口算（kouSuan）/ 搜题（yuanSouti）等，每个 App 的 JS Bridge 不同
- **多支付方式**：微信支付 / 支付宝 / iOS IAP / 0 元支付，每种方式的 API 调用路径不同
- **多业务类型**：ybc（大编程）/ ymm（小编程），对应不同的后端接口和 `extraInfo` 字段
- **复杂校验链**：登录 → 学员信息 → 家长锁 → 隐私协议 → SKU 存在性 → 赠课特权

这套逻辑 1548 次提交中有 53 次集中在 `order.ts` 一个文件，是仓库演化最激烈的区域。

---

## 2. Mixin 分层架构

```
order-common.ts（StoreOrderMixin）
  └── extends BaseOrderMixin（order.ts）
        └── extends CheckLoginMixin（checkLogin.ts）
```

| Mixin | 职责 | 来源 |
|-------|------|------|
| `CheckLoginMixin` | 检查登录状态，未登录时触发登录流程 | `checkLogin.ts` |
| `BaseOrderMixin` | 全部下单/支付逻辑（核心）| `order.ts` |
| `StoreOrderMixin` | 从 Vuex store 补充 `pageInfo`、`products`、`useMpLogin` | `order-common.ts` |

页面组件混入 `StoreOrderMixin`，相当于同时继承了三层逻辑。`order-custom.ts` 和 `order-school.ts` 是针对定制场景的子类 mixin（覆盖 `customCreateOrder` 钩子）。

---

## 3. 下单流程全链路

```
用户点击购买按钮
  │
  ▼
handleCreateOrder()          ← 入口（公开）
  ├── checkSkuExist()         → SKU 不存在 → refreshPage()
  ├── hasStudentInfo check    → 学员姓名/年级/班级/学校 未填 → showToast()
  ├── useIOSIapPay check      → iOS IAP → ybcParentLock()（家长锁）
  ├── payLoading guard        → 防重复提交
  └── afterHandleCreateOrder()

afterHandleCreateOrder()
  ├── checkLogin()            → 未登录 → 触发登录弹窗 / kit-login 组件
  ├── androidChannelReport()  → 安卓渠道回传（华为智能分包）
  ├── iosAsaReport()          → iOS ASA 渠道参数收集
  ├── payClickAdsReport()     → 广告点击回传（无需登录即上报）
  ├── agreePrivacy check      → 未勾选隐私协议 → open privacyPopup
  ├── freePurchase / rGiftPurchase → encGetGiftLessonStatus() → 检查赠课特权
  ├── payVerifiedAdsReport()  → 广告已登录回传
  ├── reportUserDevice()      → 上报用户设备
  ├── needAddress check       → 未填地址 → showToast()
  └── createOrder()

createOrder()
  ├── customCreateOrder()     ← 钩子：子类可覆盖（order-custom / order-school）
  ├── 构造 orderParams（activityId / bizType / items / extraInfos / storeParam 等）
  ├── createOrder API         → .then() → handlePay(orderId)
  └── .catch() 错误处理（完整枚举见下节）

handlePay(orderId)
  ├── 附加支付参数（couponId / coinCount / beanVoucherIds）
  └── pay(data, PayTypeMap[payType], bizType, options)
        └── utils/pay.ts（支付路由器）
```

---

## 4. 下单错误处理矩阵

`createOrder` 的 catch 是整个文件中最复杂的部分，枚举了 7 种错误场景：

| HTTP Status / 条件 | 场景 | 处理方式 |
|------------------|------|---------|
| `409 + conflictOrderIds + businessStatus=8` | 存在冲突未支付订单 | `deleteExistedOrder()` 后重试 |
| `412 + freePurchase/rGiftPurchase` | 赠课特权已失效 | `handleZeroPurchase(fail)` 跳结果页 |
| `401` | 下单接口未登录 | 重新触发登录 |
| message 含"商品发生变化" | SKU 变价 | showToast + 1秒后 refreshPage |
| message 含"活动火爆…" | 限流 | 展示 loading toast + 自动重试（最多 3 次，每次 1 秒）|
| message 含"重复购买" 等 | 正常业务拒绝 | showToast，不上报 Sentry |
| 其他 | 未知错误 | showToast + fatal Sentry 上报 + sendMessage |

**限流重试逻辑**（值得单独记录）：
```
retryTime = 0
onError("活动火爆"):
  showLoadingToast → setTimeout 1s →
    retryTime += 1
    if retryTime > 3: showErrorToast（不再重试）
    else: createOrder()（递归重试）
```

---

## 5. 支付路由器（utils/pay.ts）

`pay.ts` 是统一支付的**路由分发层**，对上层屏蔽所有端差异：

```
pay(data, payType, bizTypeNum, options)
  ├── zeroPay → zeroPay(data, bizType, options)
  ├── wxpay   → wechatPay(data, bizType, options)
  ├── alipay  → aliPay(data, bizType, options)
  └── iap     → iosIAPPay(data)
```

### 5.1 微信支付分发（handleWechatPay）

H5 微信支付需要按 `env` 参数选择不同的小程序支付页路由：

| env 值 | 跳转的小程序页面 |
|--------|--------------|
| `yfd` / `activityMP` / `databaseMP` | `/pages/pureWebviewPay/pureWebviewPay` |
| `steamMP` / `steamYmmMP` | `/pages/webviewPay/webviewPay?errorToResult=true` |
| `conanAI` / `conanParent` | `/conan-common/pages/page-pay-pure/index` |
| `tiktok` scene | `postMessage` 给父页面（iframe 场景）|
| 默认 | `/pages/pureWebviewPay/pureWebviewPay` |

### 5.2 ymm（小编程）微信支付的 payChannel/payFrom 矩阵

小编程微信支付需要传 `payChannel`（渠道号）和 `payFrom`（来源号），按 env 细分：

| 环境 | payChannel | payFrom |
|------|-----------|--------|
| 普通 H5 微信外 | 3 | — |
| 微信内 H5 | 4 | 4 |
| 辅导 App | 102 | 9 |
| 小程序（yfd）| 5 | 11 |
| 小程序（steamMP）| 5 | 12 |
| 小程序（activityMP）| 5 | 14 |
| 小程序（conanGrowth）| 5 | 16 |
| 小程序（conanAI）| 5 | 17 |
| 小程序（conanParent）| 5 | 20 |
| hdzxMP（助力营）| 5 | 21 |
| xybcMP（探索营）| 5 | 22 |
| ybcwxMP（训练营）| 5 | 23 |
| 微信小程序（原生）| 5 | 18 |
| YFDPad（辅导 iPad）| 104 | 8/9/0 |

这个矩阵记录了公司内部每个投放环境的支付参数映射，是"业务知识"而非"通用设计"。

### 5.3 支付宝支付

- `ybc`：默认用 `ybcAliPay`；猿编程 App 内用 `ybcAliPayV2`；store 场景用 `ybcAliPayForStore`
- `ymm`：调 `ymmAliPay`；辅导 App 内设置 `payChannel=103, payFrom=10`
- H5 浏览器端：动态插入 form 表单并 submit（`document.forms[0].submit()`）

### 5.4 iOS IAP 支付

仅在猿编程 App iOS 端（`isYBC && isiOS`）且 `pageParams.useIAP=true` 时启用，通过 `ybcIosIAPPay` 调用 JS Bridge，需要提前用 `getAppleProductId(skuId)` 获取苹果商品 ID。

---

## 6. 支付后处理（多端差异最显著的部分）

### 小程序支付后
```js
handleMpPaySuccess(orderId)
  → uni.redirectTo('/pages/webview/webview?webviewUrl=' + encodeURIComponent(payResultUrl))
  （小程序通过 webview 页承载 H5 结果页）
```

### H5 支付后（isYBC App 内）
```
pollingCheckOrderPaid()（轮询，最多 5 次，每次 500ms）
  → 支付确认 → pollingCheckABTest()（ABTest：跳普通结果页 or 跳微信添加老师）
    → paidResultPageAbTestResult === 1 → gotoPayResult()
    → paidResultPageAbTestResult === 2 → getPayResult()（加载订单详情 → 开启微信小程序）
```

### H5 支付后（微信内 / 其他 App）
```
handlePaySuccess()
  → 微信内 / 0元 → window.location.replace(payResultUrl)
  → 微信外 H5 有 mweb_url → window.location.replace(mweb_url + redirect_url)
```

---

## 7. 价格计算体系

```
salePrice（展示价格）
  = useDiscount ? skuInfo.salePrice : pageInfo.price/100 + luckyDiscount

finalPrice（最终扣款价格）
  = salePrice - couponInfo.couponPrice - coinCount - beanVoucherPrice
  （结果 < 0 时取 0）

三种抵扣：
  - coupon（真优惠券/假优惠券 luckyDiscount）
  - coin（金币，单位：元，100coin = 1元）
  - beanVoucher（猿豆代金券，VOS列表，分 source=2 和 source=3 两种）
```

**两种价格策略**（`PriceStrategy`）：
- `DISCOUNT`：真优惠券，从接口拉取，`useDiscount=true`，三种抵扣全部生效
- `CUSTOM`：自定义价格，`luckyDiscount` 是"假优惠券"（只是视觉上的折扣展示）

---

## 8. extraInfos：下单时的广告回传参数

`getReportParams()` 是广告投放回传的核心，把当前页面的所有追踪参数打包进下单接口的 `extraInfos`：

| 字段 | 来源 | 说明 |
|------|------|------|
| `clickId` | H5: cookie / MP: pageParams | 广告点击 ID |
| `url` / `adUrl` | H5: cookie 或 location.href | 广告来源 URL |
| `enterId` | pageParams | 进入 ID |
| `requestId` | pageParams | ABTest 请求 ID |
| `fromPostId` | pageParams | 海报 AB 测 |
| `encStartUserId` | pageParams.encUserId | 老带新裂变 |
| `ua` | device.ts | UA 字符串 |
| `wechatOpenId` / `wechatAppId` | store.userInfo | 小程序投放回传 |
| `latLng` | sessionStorage | 地推定位 |
| `queryString` | qs.stringify(pageParams) | 完整 URL 参数 |
| `studentName/Grade/Class/SchoolId` | store.studentInfo | 学员信息（如有）|

---

## 9. customCreateOrder 钩子（扩展点）

`BaseOrderMixin.createOrder()` 在执行前调用 `customCreateOrder()`，默认返回 false（走标准逻辑）。子类可以覆盖此方法实现完全自定义的下单路径：

```ts
// 在 order-custom.ts 或 order-school.ts 里
customCreateOrder(): boolean {
  // 处理特殊逻辑
  this.createSpecialOrder()
  return true  // 返回 true = 阻止标准 createOrder 执行
}
```

这是唯一正确的扩展方式，避免直接覆盖 `createOrder()` 导致校验链断裂。

---

## 10. 已知痛点

| 痛点 | 现状 | 改进方向 |
|------|------|---------|
| order.ts 1643 行 | 单文件过长，所有逻辑耦合 | 按职责拆分（价格计算、广告回传、支付后处理各独立模块）|
| pay.ts 的 env/payChannel 矩阵 | 硬编码映射关系，新增投放环境需改源码 | 配置化（从后端下发或从 config.ts 集中维护）|
| H5 微信支付通过 `env` 区分小程序 | env 字符串枚举散落在多处 | 统一为 TypeScript enum，消除魔法字符串 |
| 限流重试用 retryTime 实例变量 | 并发情况下可能失控 | 改用更健壮的 retry 工具函数，附带 exponential backoff |
| mixin 继承链（Vue 2）| CheckLogin → BaseOrder → StoreOrder → 页面组件，调用链难以追踪 | Vue 3 迁移后改为 composable，每个关注点独立 hook |

---

## 11. 可复用的设计模式

> 以下内容脱离 ada-sale-activity 后仍然成立，适合回流到 wiki。

**"校验链"模式**（适用于任何多步骤表单提交）：
```
入口方法 → 前置校验（SKU/学员信息/家长锁/防重复）→ 核心逻辑 → 错误处理
```
每个校验步骤在失败时直接 return，不嵌套 if-else，保持线性可读。

**"广告回传与业务逻辑分离"**：
- `payClickAdsReport`（点击时，无需登录）和 `payVerifiedAdsReport`（已登录时）分两个时间点上报
- 两个上报都用 `.catch` 静默处理，不阻塞主流程

**"支付路由器"模式**：
- 一个统一的 `pay()` 函数，入参是 `payType + bizType + options`
- 内部按 payType 分发到各自实现，调用方无需感知底层差异
- 适合所有需要支持多种支付方式的场景

**Vue 2 Mixin 分层的局限**（反模式记录）：
- Mixin 的属性/方法来源不透明，`this.xxx` 来自哪一层 mixin 需要逐个查找
- 多层继承的 `@Watch` 会叠加，容易产生意外的多次触发
- Vue 3 的 composable 是正确的替代方案：每个关注点（useOrder / usePay / useLogin / useDiscount）独立暴露，来源清晰
