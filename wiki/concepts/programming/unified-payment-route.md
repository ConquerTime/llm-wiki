---
title: 统一支付路由设计
type: concept
subtype: programming
tags: [programming, architecture, backend, horizon-web-commerce]
created: 2026-04-16
updated: 2026-04-27
sources: []
---

# 统一支付路由设计

> 将支付能力从业务页面抽取为独立的公共支付路由，让多个业务场景共享同一套支付渠道选择、发起支付、回调轮询能力。

## 是什么

在电商系统中，多个业务线（正价课、体验课、会员等）都需要支付能力。如果每个业务各建一个支付页，会重复实现支付渠道选择、第三方支付跳转、回调轮询等逻辑。统一支付路由的核心思想：**支付页只负责"收钱"，不关心"卖什么"**。

```
  业务方 A ──┐                ┌─── 微信支付
  业务方 B ──┼──▶ /common/pay ──┤
  业务方 C ──┘                └─── 支付宝
```

业务方只需要：创建订单 → 拿到订单号 → 跳转公共支付页。

## 为什么重要

- **复用**：支付渠道选择、轮询确认、错误处理只写一遍
- **一致性**：所有业务的支付体验统一
- **外部约束**：微信支付有授权目录白名单限制（最多 5 个），统一入口可节省白名单名额

## 关键设计决策

以下是设计统一支付路由时必须面对的决策点，以及每个决策的核心权衡逻辑。

### 决策 1：入参协议 — 状态怎么传给支付页

支付页有两种进入方式，技术约束完全不同：

| 进入方式 | 特点 |
|---------|------|
| 站内跳转（用户点"去支付"） | JS 内存可用，能传复杂对象 |
| 第三方回调（微信支付完跳回来） | JS 内存已丢失，只能靠 URL 恢复 |

**三种方案的权衡：**

- **query params**：最简单，URL 自包含，但有 open redirect 风险（需加 `isInternalPath` 校验）
- **sessionStorage**：回调后能完整恢复 UI，但微信内置浏览器跨 app 跳转可能清空存储
- **后端查询**：最健壮，但需要新接口，且多一次网络请求

**推荐**：站内跳转用 `location.state`，第三方回调用 query params（最小集）。这是成本最低且够用的方案。回调时用户只会短暂看到"确认中"状态，不需要完整 UI。

### 决策 2：鉴权 — 谁来保证用户已登录

支付接口需要 userId，未登录就无法工作。关键问题：支付页自己管登录，还是信任调用方？

**三种方案的权衡：**

- **业务方负责，支付页裸奔**：最简单，但第三方回调时 session 过期会白屏
- **支付页内置 AuthGuard**：最安全，但需要通用登录体系（如果各业务登录方式不同，成本很高）
- **轻量断言 + 降级提示**：业务方保证登录，支付页兜底检查 —— 未登录不尝试修复，展示友好提示

**推荐**：轻量断言。原因：
1. 第三方回调 session 过期是小概率事件（支付通常几十秒内完成）
2. 即使发生，用户的钱已付，后端已更新状态，不会丢钱
3. 内置 AuthGuard 要求统一登录体系，这是更大的架构改造

### 决策 3：商品信息展示 — 支付页需要多了解业务

支付页需要展示"用户在买什么"，但不应该知道太多业务细节。

**三种方案的权衡：**

- **固定模板**（`title + subtitle + price`）：简单，覆盖大多数场景
- **传入 ReactNode**：最灵活，但业务方需要关心支付页的布局
- **配置式**（`{ lines: [{label, value}] }`）：灵活度适中，但增加协议复杂度

**推荐**：固定模板。业务方把业务特定信息拼装成通用字段（如 `classCount: 8` → `subtitle: "8 课时"`），支付页只管渲染。

### 决策 4：returnUrl 指向哪里

第三方支付完成后的回调 URL 是个关键设计点。直觉想法是"直接跳到业务成功页"，但这行不通：

**微信/支付宝的 returnUrl 语义是"用户离开了支付页"，不是"支付成功"。** 用户取消、失败、超时都会跳回 returnUrl。

因此 returnUrl 必须指向支付页自身，由支付页轮询确认到账后再跳转到业务成功页。

```
  ✗ 错误：returnUrl → /course/success/1  （取消也会跳到成功页）
  ✓ 正确：returnUrl → /common/pay?fromPay=1&...  （支付页轮询确认后再跳）
```

## 通用入参接口设计

```typescript
interface PaymentLocationState {
  // 支付必须
  orderId: number;
  boltBizId: number;
  boltPayOrderId: number;
  // 展示信息
  amountCents: number;
  productName: string;
  subtitle?: string;
  listPriceCents?: number;
  // 路由控制
  returnPath: string;   // 支付成功后跳哪
  cancelPath: string;   // 异常时回退到哪
}
```

## 项目实践

### horizon-web-commerce
- 公共支付页路由：`/#/common/pay`，从 `CoursePaymentPage` 抽取
- 原课程支付页退化为薄壳（仅做旧 returnUrl 兼容重定向）
- 通用 hook `useBoltPayment` 和 `PaymentMethodSelector` 组件从 course 目录提升到 common 目录
- 设计文档：`openspec/changes/unified-payment-page/`

#### 2026-04-27 更新：白屏修复与状态机重构

上线数月后暴露出新问题与结构债：

- **bug**：微信 UA + 非授权态进入支付页 → `useWechatAuth` 触发 `window.location.replace` 跳 OAuth → 回跳后 `location.state` 丢失 → 白屏
- **结构债**：`UnifiedPaymentPage` 膨胀至 312 行；`useBoltPayment` 参数 17 个；上下文字段逐字段三元选源

clean-code 审查识别出四类反模式（详见 [[react-page-state-antipatterns|React 页面状态管理反模式与重构]]）：布尔语义过载、内存态单源、隐式状态机、字段级三源合并。

落地为两个 OpenSpec change：

- `fix-payment-oauth-redirect-whitescreen` — 最小修复：引入 `phase: 'entry'|'paying'` 字段穿透整页跳转，`fromPay` 拆为 `isReturningFromPayment` + `hasRestorableContext`
- `refactor-payment-page-state-machine` — 结构重构：显式 phase 状态机 + `usePaymentContext` / `usePaymentFlow` / `useCancelOrder` / `PaymentLayout` 分层

**对原决策 1（入参协议）的补充**：当时只讨论了 query / state / session 三源，没考虑"OAuth 整页跳转"这类链路——此时所有入参源都不可信，必须由页面在 mount 时写入 `phase='entry'` 的 session 作为锚点。sessionStorage 不只是"第三方回调兜底"，也是"穿越任何整页跳转"的通用锚。

## 相关概念

- [[react-page-state-antipatterns|React 页面状态管理反模式与重构]] — 本页后续暴露的四类反模式与重构对策
- [[open-redirect|Open Redirect]] — 统一支付路由中 returnPath/cancelPath 的安全防护
- [[oauth-state-parameter|OAuth state 参数]] — 触发整页跳转的典型链路
- [[message-queue|消息队列]] — 另一种系统间解耦模式
