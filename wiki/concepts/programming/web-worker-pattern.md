---
title: Web-Worker Pattern
type: concept
subtype: programming
tags: [programming, architecture, cloud-deployment]
created: 2026-05-01
updated: 2026-05-01
sources:
  - [[../../sources/articles/kaigao-ecs-deployment|kaigao ECS 部署方案]]
---

> Web-Worker Pattern：将 HTTP 接口（Producer）和后台 Worker（Consumer）分离的架构模式，同一镜像通过不同 command 启动不同角色。

## 定义

Web-Worker Pattern 是「API + Background Worker」架构的正式名称：
- **Web/API 层**：HTTP 接口处理请求（producer），接收用户请求后立即返回，异步触发任务
- **Worker 层**：异步消费任务队列（consumer），处理长任务（AI 推理、邮件发送、数据处理等）
- **Single-image, multi-role**：同一镜像通过 `docker-compose` 的 `command` 字段指定不同入口

这是业界主流做法：Rails/Sidekiq、Django/Celery、Node/BullMQ 都是这个模式。

## 何时使用

适合以下场景：
- 有**长任务**（AI 推理、批量处理）需要异步执行
- Worker 需要和 API 共享 schema、domain service、类型
- 希望**单一 CI 构建**一次镜像，部署多角色
- 需要 Worker **独立重启**（不牵连 API）

不适合：
- Worker 有**独立重依赖**（ML 库、FFmpeg 等）
- 镜像超过 1GB
- 不同团队有**独立发布周期**

## docker-compose 示例

```yaml
services:
  api:
    image: myapp:latest
    command: ["node", "dist/server.js"]
    ports:
      - "8080:8080"

  worker:
    image: myapp:latest
    command: ["node", "dist/worker.js"]
    depends_on:
      api:
        condition: service_healthy

  reduce-worker:
    image: myapp:latest
    command: ["node", "dist/reduce-worker.js"]
    depends_on:
      api:
        condition: service_healthy
```

关键设计：
- `depends_on: api: condition: service_healthy` 确保 Worker 等 API 完成数据库迁移后才启动
- Worker 之间独立运行，`restart: always` 自动重启
- API 不暴露端口（不写 `ports` 字段），只在 docker 网络内可达

## 健康检查设计

Worker 通常无 HTTP 端口，健康检查依赖：
- API 提供 `/health` 端点
- `depends_on: api: condition: service_healthy` 链式依赖
- BullMQ 的 `completed` / `failed` 事件驱动监控

## 队列选型

| 队列 | 语言/平台 | 特点 |
|------|----------|------|
| BullMQ | Node.js | Redis-based，功能完整 |
| Sidekiq | Ruby | 线程安全，生产验证 |
| Celery | Python | 分布式支持强 |
| RQ | Python | 轻量，Redis-based |

## 与 [[monolith-async-worker]] 的关系

[[monolith-async-worker]] 是更宏观的架构描述（单体应用内嵌异步 Worker），而 Web-Worker Pattern 是具体的**进程分离模式**。两者可以结合：
- 单体内嵌 `child_process.spawn` → 进程耦合，崩一个影响另一个
- docker-compose 独立容器 → 完全隔离，独立扩缩容

## 参见

- [[backend-architecture]] — 后端架构模式
- [[cloud-deployment]] — Docker/K8s/ IaC 等部署知识
- [[message-queue]] — BullMQ 消息队列深入知识
