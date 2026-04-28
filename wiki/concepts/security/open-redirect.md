---
title: Open Redirect（开放重定向漏洞）
type: concept
subtype: security
tags: [programming, security]
created: 2026-04-16
updated: 2026-04-16
sources: []
---

# Open Redirect（开放重定向漏洞）

> 当应用从用户可控的输入（URL 参数、表单字段）中读取跳转目标，且未校验其合法性时，攻击者可构造恶意链接将用户重定向到外部站点。

## 是什么

Open Redirect 是 OWASP Top 10 中的常见漏洞。攻击模式：

```
正常链接：https://example.com/pay?returnPath=/course/success/1
恶意链接：https://example.com/pay?returnPath=https://evil.com/steal-token
```

用户信任 `example.com` 域名点击链接，完成操作后被跳转到攻击者控制的站点。常被用于：
- 钓鱼攻击（伪造登录页骗取凭证）
- Token 窃取（OAuth callback 场景）
- 信任链利用（用户看到的是可信域名）

## 为什么重要

任何包含"操作完成后跳转回来"逻辑的页面都可能暴露此漏洞，典型场景：
- 登录页的 `redirect` / `next` 参数
- 支付回调的 `returnUrl` / `cancelUrl` 参数
- OAuth 的 `redirect_uri` 参数

## 防护方法

### 方法 1：白名单校验（最严格）

```typescript
const ALLOWED_PREFIXES = ['/course/', '/trial/', '/common/'];
function isAllowedPath(path: string): boolean {
  return ALLOWED_PREFIXES.some(p => path.startsWith(p));
}
```

### 方法 2：结构校验（推荐，通用性好）

只允许以 `/` 开头且不含 `//` 的站内相对路径：

```typescript
function isInternalPath(path: string): boolean {
  return path.startsWith('/') && !path.includes('//');
}
```

`//evil.com` 会被浏览器解析为 protocol-relative URL（等同于 `https://evil.com`），所以必须排除 `//`。

### 方法 3：不传跳转路径

从根源消除 —— 跳转目标不由 URL 参数决定，而是由后端状态或前端路由映射表决定。但灵活性较低。

## 项目实践

### horizon-web-commerce
- 公共支付页 `/common/pay` 的 `returnPath` 和 `cancelPath` 通过 query params 传递（微信 H5 支付回调场景），需防护 open redirect
- 防护方案：`utils/isInternalPath.ts` — 采用方法 2，校验以 `/` 开头且不含 `//`
- 设计文档：`openspec/changes/unified-payment-page/design.md` Decision 1

## 相关概念

- [[message-queue|消息队列]] — 另一个需要安全考量的系统间通信场景
