# 业务知识 #2：支付参数体系

> ada-sale-activity 中下单与支付链路的全部业务参数：支付类型、App 标识、多端分发、payChannel/payFrom 矩阵。

---

## 1. 支付类型（payType）

| payType | 说明 | 适用条件 |
|---------|------|---------|
| `wxpay` | 微信支付 | H5 微信内 / 小程序 / App 内微信 |
| `alipay` | 支付宝 | H5 浏览器 / App 内支付宝 |
| `iap` | iOS 内购（Apple IAP）| isYBC + isiOS + pageParams.useIAP=true |
| `zeroPay` / `freePurchase` | 0 元支付 | 免费课程 / 赠课特权 |

支付路由器入口：`utils/pay.ts`  `pay(data, PayTypeMap[payType], bizType, options)`

---

## 2. 业务类型（bizType）

| bizType | 对应业务 | 说明 |
|---------|---------|------|
| `ybc` | 猿编程（大编程） | 默认业务类型 |
| `ymm` | 小猿口算 / 小编程 | 独立后端接口 + 独立 payChannel/payFrom |

`bizType` 决定：
1. 调用哪个下单接口（不同 API endpoint）
2. 微信支付时的 `payChannel` 和 `payFrom` 值（见第 4 节）
3. 支付宝使用哪个 SDK 方法（`ybcAliPay` vs `ymmAliPay`）

---

## 3. App/端标识（env 含义）

`env`（来自后端下发的 `pageInfo.env` 或 URL 参数）标识当前落地页运行的宿主环境：

| env 值 | 宿主 | 平台类型 |
|--------|------|---------|
| `yfd` | 猿辅导 App（Android/iOS）| App 内 H5 |
| `activityMP` | 猿辅导活动小程序 | 微信小程序 |
| `databaseMP` | 题库小程序 | 微信小程序 |
| `steamMP` | steam 小程序（大编程）| 微信小程序 |
| `steamYmmMP` | steam ymm 小程序 | 微信小程序 |
| `conanAI` | 柯南 AI 小程序 | 微信小程序 |
| `conanParent` | 柯南家长端小程序 | 微信小程序 |
| `conanGrowth` | 柯南成长记录小程序 | 微信小程序 |
| `hdzxMP` | 助力营小程序 | 微信小程序 |
| `xybcMP` | 探索营小程序 | 微信小程序 |
| `ybcwxMP` | 训练营小程序 | 微信小程序 |
| `YFDPad` | 猿辅导 iPad App | App 内 H5 |
| `tiktok` | 字节跳动头条系 App | H5 iframe 场景 |
| （空/默认）| 普通 H5 浏览器 | 微信内 H5 或微信外 H5 |

---

## 4. ymm 微信支付 payChannel/payFrom 矩阵

小编程（ymm）微信支付需要传 `payChannel` + `payFrom` 两个参数，按宿主环境细分：

| 宿主环境 | payChannel | payFrom | 说明 |
|---------|-----------|--------|------|
| 普通 H5（微信外）| 3 | — | 标准 H5 |
| 微信内 H5 | 4 | 4 | JSAPI 支付 |
| 猿辅导 App（iOS/Android）| 102 | 9 | App 内 H5 |
| 小程序（yfd）| 5 | 11 | |
| 小程序（steamMP）| 5 | 12 | |
| 小程序（activityMP）| 5 | 14 | |
| 小程序（conanGrowth）| 5 | 16 | |
| 小程序（conanAI）| 5 | 17 | |
| 微信原生小程序 | 5 | 18 | |
| 小程序（conanParent）| 5 | 20 | |
| 小程序（hdzxMP 助力营）| 5 | 21 | |
| 小程序（xybcMP 探索营）| 5 | 22 | |
| 小程序（ybcwxMP 训练营）| 5 | 23 | |
| YFDPad（辅导 iPad）| 104 | 8 / 9 / 0 | 按具体场景 |

**规律**：
- `payChannel=3`：纯 H5 浏览器
- `payChannel=4`：微信内 H5（JSAPI）
- `payChannel=5`：所有微信小程序
- `payChannel=102`/`104`：猿辅导 App

---

## 5. H5 微信支付跳转的小程序页面路由

微信内 H5 支付需要跳到小程序的支付页（绕开 H5 微信支付的限制），按宿主环境选择不同小程序页面：

| env 值 | 跳转页面 |
|--------|---------|
| `yfd` / `activityMP` / `databaseMP` | `/pages/pureWebviewPay/pureWebviewPay` |
| `steamMP` / `steamYmmMP` | `/pages/webviewPay/webviewPay?errorToResult=true` |
| `conanAI` / `conanParent` | `/conan-common/pages/page-pay-pure/index` |
| `tiktok` 场景 | `postMessage` 给父页面（iframe 场景）|
| 默认 | `/pages/pureWebviewPay/pureWebviewPay` |

---

## 6. 支付宝分发逻辑

| bizType | 宿主 | 调用方法 |
|---------|------|---------|
| `ybc` | 默认 | `ybcAliPay` |
| `ybc` | 猿编程 App 内 | `ybcAliPayV2` |
| `ybc` | store 场景 | `ybcAliPayForStore` |
| `ymm` | 默认 | `ymmAliPay`（payChannel=—）|
| `ymm` | 辅导 App 内 | `ymmAliPay`（payChannel=103, payFrom=10）|
| 任意 | H5 浏览器端 | 动态插入 `<form>` 并 `document.forms[0].submit()` |

---

## 7. iOS IAP 支付条件

启用条件（全部满足）：
1. `isYBC`（猿编程 App）= true
2. `isiOS` = true
3. `pageParams.useIAP` = `'true'`（字符串）

执行流程：
```
getAppleProductId(skuId)   → 获取苹果商品 ID
  → ybcIosIAPPay(appleProductId, orderId, ...)  → JS Bridge
```

---

## 8. 价格计算体系

```
salePrice（展示价格）
  = useDiscount ? skuInfo.salePrice : pageInfo.price/100 + luckyDiscount

finalPrice（最终扣款价格）
  = salePrice - couponInfo.couponPrice - coinCount - beanVoucherPrice
  （结果 < 0 时取 0）
```

**两种价格策略（PriceStrategy）**：

| 策略 | useDiscount | 来源 | 抵扣是否全部生效 |
|------|------------|------|--------------|
| `DISCOUNT` | true | 从接口拉取的真实优惠券 | 是（coupon + coin + beanVoucher）|
| `CUSTOM` | false | `luckyDiscount` 是假优惠券（只是视觉折扣）| 是（但 coupon 部分实际为 luckyDiscount）|

**三种抵扣类型**：

| 抵扣 | 单位 | 说明 |
|------|------|------|
| coupon | 元 | 真优惠券（从接口拉取）|
| coin | 元（100coin = 1元）| 金币 |
| beanVoucher | 元 | 猿豆代金券，分 source=2 和 source=3 两种，来自 VOS 列表 |

---

## 9. 广告回传参数（extraInfos）

下单接口的 `extraInfos` 字段携带完整广告归因参数，由 `getReportParams()` 构造：

| 字段 | 来源 | 说明 |
|------|------|------|
| `clickId` | H5: cookie / MP: pageParams | 广告点击 ID |
| `url` / `adUrl` | H5: cookie 或 location.href | 广告来源 URL |
| `enterId` | pageParams | 进入 ID |
| `requestId` | pageParams | ABTest 请求 ID |
| `fromPostId` | pageParams | 海报 AB 测 |
| `encStartUserId` | pageParams.encUserId | 老带新裂变标识 |
| `ua` | device.ts | User-Agent 字符串 |
| `wechatOpenId` / `wechatAppId` | store.userInfo | 小程序投放回传 |
| `latLng` | sessionStorage | 地推定位坐标 |
| `queryString` | qs.stringify(pageParams) | 完整 URL 参数快照 |
| `studentName/Grade/Class/SchoolId` | store.studentInfo | 学员信息（如已填写）|
