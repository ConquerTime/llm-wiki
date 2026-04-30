---
title: 校验链模式
type: concept
subtype: programming
tags: [programming, architecture, clean-code]
created: 2026-04-29
updated: 2026-04-29
sources: []
---

# 校验链模式

> 在执行核心业务逻辑前，将多个前置条件检查串联为一条线性链，每个节点失败时直接 return，不嵌套 if-else，保持流程可读性。

## 是什么

校验链（Validation Chain）是一种**程序结构模式**，适用于"点击提交 → 多步骤前置检查 → 核心操作"这类流程：

```
入口方法
  ├── 校验 1：前置条件 A 不满足 → return（早退）
  ├── 校验 2：前置条件 B 不满足 → return（早退）
  ├── 校验 3：前置条件 C 不满足 → return（早退）
  └── 核心操作（仅在所有校验通过后才执行）
```

与嵌套 if-else 的区别：

```ts
// ❌ 嵌套（难以追踪，缩进越来越深）
if (condA) {
  if (condB) {
    if (condC) {
      doCore()
    } else { showError('C') }
  } else { showError('B') }
} else { showError('A') }

// ✅ 校验链（线性，每个校验独立）
if (!condA) { showError('A'); return }
if (!condB) { showError('B'); return }
if (!condC) { showError('C'); return }
doCore()
```

## 关键特征

1. **早退（Early Return）**：校验失败立即 return，不继续向下
2. **线性结构**：每个校验节点平行，不嵌套
3. **单一职责**：每个校验节点只负责一个条件，处理自己的错误提示
4. **核心逻辑隔离**：`doCore()` 只在链的末尾，不混入校验逻辑

## 实战案例：电商下单流程

ada-sale-activity 的 `handleCreateOrder()` 是校验链的完整实现：

```
handleCreateOrder()
  ├── checkSkuExist() 失败 → refreshPage()；return
  ├── hasStudentInfo 未填 → showToast('请填写学员信息')；return
  ├── useIOSIapPay → ybcParentLock() 家长锁；return
  ├── payLoading === true → return（防重复提交）
  └── afterHandleCreateOrder()

afterHandleCreateOrder()
  ├── checkLogin() 未登录 → 触发登录弹窗；return
  ├── agreePrivacy === false → open privacyPopup；return
  ├── freePurchase → encGetGiftLessonStatus() 检查赠课；return（跳赠课路径）
  └── createOrder()
```

7 个前置校验，全部线性排列，`createOrder()` 只在通过全部校验后才执行。

## 变体：异步校验链

前置校验如果是异步操作（如网络请求），可以用 `async/await` 保持线性：

```ts
async function handleSubmit() {
  const skuValid = await checkSkuExist()
  if (!skuValid) { refreshPage(); return }

  const loginOk = await checkLogin()
  if (!loginOk) { showLoginModal(); return }

  await createOrder()
}
```

## 与责任链模式（Chain of Responsibility）的区别

| 维度 | 校验链 | 责任链（GoF）|
|------|--------|------------|
| 目的 | 前置条件检查，全部通过才继续 | 请求沿链传递，找到能处理的节点 |
| 失败语义 | 失败即终止，向用户报错 | 失败即传递给下一个处理者 |
| 核心操作 | 在链的末尾执行 | 分散在各处理者节点 |
| 典型场景 | 表单提交前校验 | 日志处理、审批流 |

## 适用场景

- 表单提交前的多步骤校验（登录状态 / 字段完整性 / 业务规则）
- 任何"多个前置条件 → 一个核心操作"的流程
- 需要向用户提供具体失败原因的场景

## 不适用场景

- 校验之间有复杂依赖关系（需要 A 的结果才能执行 B 的校验）→ 考虑状态机
- 校验条件非常多且动态变化 → 考虑规则引擎

## 相关概念

- [[design-patterns|设计模式]] — GoF 模式总览；本模式接近 Template Method 变体
- [[clean-code|Clean Code]] — Early Return 是整洁代码的核心实践之一
- [[unified-payment-route|统一支付路由]] — 另一种电商下单链路的架构模式
