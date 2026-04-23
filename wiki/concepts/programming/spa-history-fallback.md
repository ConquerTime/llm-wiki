---
title: SPA History 路由与服务端 Fallback
type: concept
subtype: programming
tags: [spa, react-router, browser-router, nginx, deployment, horizon-admin-web-commerce]
created: 2026-04-23
updated: 2026-04-23
sources: []
---

# SPA History 路由与服务端 Fallback

> BrowserRouter 使用 HTML5 History API，URL 看起来像真实服务端路径，刷新时浏览器会向服务器请求该路径，服务器必须配置 fallback 返回 `index.html`，否则 404。

## 是什么

单页应用（SPA）有两种路由模式：

| 模式 | 实现 | URL 示例 | 服务端需配置 |
|---|---|---|---|
| Hash 路由 | `HashRouter` | `/#/products` | 不需要 |
| History 路由 | `BrowserRouter` | `/products` | **需要** |

**Hash 路由**：`#` 后面的内容浏览器不发给服务器，刷新时服务器只看到 `/`，返回 `index.html`，前端 JS 再解析 hash 部分。

**History 路由**：URL 是真实路径（如 `/landing-pages/123`）。刷新时浏览器向服务器 GET `/landing-pages/123`，但服务器没有这个文件，返回 404。

## 为什么重要

在本地开发时 Vite dev server 会自动处理 fallback，所以感觉一切正常。但部署到生产环境（nginx、CDN、静态托管）后，如果没有配置 fallback，只有根路径能正常访问，直接访问子路由或刷新页面都会 404。

## 基本用法

### Nginx

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

`try_files` 先尝试找真实文件，找不到就回退到 `/index.html`。

### Apache `.htaccess`

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

### Express（Node.js）

```js
app.get('*', (req, res) => {
  res.sendFile(path.resolve(__dirname, 'dist', 'index.html'));
});
```

注意：静态资源路由（`/api`、`/assets`）必须放在通配符路由**之前**，否则 API 请求也会被返回 `index.html`。

### Netlify

在 `public/_redirects` 文件中：

```
/*  /index.html  200
```

### Vercel

在 `vercel.json` 中：

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

## 项目实践

### horizon-admin-web-commerce（admin-growth）

- `apps/admin-growth/src/App.tsx:3` — 使用 `BrowserRouter`，路由形如 `/landing-pages`、`/leads/:id`
- 对比：`apps/admin-commerce/src/App.tsx:4` — 使用 `HashRouter`，路由形如 `/#/products`
- **需确认**：growth 的部署 nginx/CDN 配置是否有 `try_files $uri $uri/ /index.html`

## 相关概念

- [[programming/canary-deployment|金丝雀部署]] — 同属部署相关概念
