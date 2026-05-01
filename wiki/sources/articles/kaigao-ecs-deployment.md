---
title: kaigao ECS 部署方案与迁移配置经验
type: source
subtype: article
date: 2026-04-20
created: 2026-05-01
updated: 2026-05-01
tags: [programming, cloud-deployment, devops]
sources:
  - ../../../raw/articles/kaigao-ecs-deployment.md
---

> kaigao 项目从阿里云 SAE 迁移到 ECS + docker-compose 的完整过程记录，含架构决策、CI/CD 分工和费用对比。

## 核心内容

### 迁移原因

1. **配置复杂**：SAE 控制台 NAT 网关 / CLB / 安全组 / 网关路由多处配置
2. **成本偏高**：两个 SAE 应用月费 200-400 元，对日访问量仅几万的早期项目不经济
3. **Worker 耦合**：Worker 通过 `child_process.spawn` 嵌在 API 进程内，无法独立重启

迁移后计算成本降至约 **100 元/月**，Worker 独立容器。

### 服务结构

| 角色 | 入口 | 说明 |
|------|------|------|
| web | Next.js standalone :3000 | SSR 前端 + API 代理层 |
| api | Hono (Node.js) :8080 | HTTP 业务接口，无端口暴露到宿主机 |
| worker | BullMQ Worker | 全文生成（AI 长任务，并发 3） |
| reduce-worker | BullMQ Worker | 降重任务（并发 2） |

**关键发现**：前端所有 API 请求走相对路径 `/api/xxx`，由 Next.js 内置的 catch-all 代理（`app/api/[...proxy]/route.ts`）转发到后端 Hono。浏览器不直接访问后端，ALB 只需指向 web:3000。

### 部署架构

```
Internet → ALB (:443 HTTPS) → ECS 2C4G (docker-compose)
                                   ├── web :3000
                                   └── api :8080 (docker内网)
                                         ├── worker (无端口)
                                         └── reduce-worker (无端口)
```

### docker-compose.prod.yml 要点

- `api` 服务不写 `ports` 字段 → 不暴露到宿主机
- `worker`/`reduce-worker` 用 `depends_on: api: condition: service_healthy` 等 API 完成数据库迁移
- `API_BASE_URL: "http://api:8080"` 使用 docker service name 寻址

### 代码改动

1. **从 server.ts 移除 spawn worker**：`startWorker()` 删除，改由 docker-compose 独立容器管理
2. **tsup 补全 reduce-worker 入口**：entry 加入 `src/reduce-worker.ts`
3. **API Dockerfile 安装 curl**：alpine 镜像默认无 curl，healthcheck 需要

### ALB 配置

只需一个监听器 + 一个服务器组指向 web:3000。不需要按路径分流 `/api/*` → api，因为 Next.js 代理层处理了。

### CI/CD 分工

| 系统 | 职责 | 触发 |
|------|------|------|
| GitHub Actions | PR 质量门禁（format/lint/type-check/test） | PR 到 main/feature/* |
| 云效 Flow | CD（构建镜像 → 推送 ACR → SSH 部署 ECS） | push to main |

云效 Flow 在阿里云内网，推 ACR 比 GitHub runner 跨境快，且原生支持主机部署。

### 费用对比

| 项 | SAE 方案 | ECS 方案 |
|----|---------|---------|
| 计算 | 200-400/月 | **100/月** |
| ALB | 10-20/月 | 10-20/月 |

### 迁移顺序（可回滚）

1. 代码改动
2. ECS 购买、安装 Docker、上传配置、手动验证
3. ALB 新建服务器组指向 ECS，不切流量
4. ALB 转发规则切换（此时可立即回切）
5. 验证后下线 SAE
6. 建云效 Flow 流水线

## 提到的概念

- [[cloud-deployment|云服务部署]] — docker-compose、ALB、安全组配置
- [[message-queue|消息队列（BullMQ）]] — BullMQ Worker 异步任务模式
- [[backend-architecture|后端架构]] — 单体 + 异步 Worker 架构模式

## 补充说明

这是项目专属文档（kaigao 项目），但其中的「Web-Worker 架构模式」「Single-image, multi-role」「docker-compose 多角色同一镜像」是通用 DevOps 模式，可归档到 [[cloud-deployment]] 或单独的概念页。
