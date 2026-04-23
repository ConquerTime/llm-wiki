---
title: Monolith with Async Worker
type: concept
subtype: programming
tags: [architecture, monolith, async-worker, message-queue, llm-wiki]
created: 2026-04-17
updated: 2026-04-17
sources: []
---

# Monolith with Async Worker

> 单体应用 + 异步工作进程的架构模式：主体是单体应用（Monolith），通过消息队列将耗时任务卸载到独立的 Worker 进程异步处理。

## 是什么

Monolith with Async Worker 不是一个严格的学术术语，而是业界广泛使用的**架构模式描述**。它指的是：

- **主进程**：单体 Web Server，处理 HTTP 请求，同步返回响应
- **消息队列**：Redis / RabbitMQ / Kafka 等，作为任务中转
- **Worker 进程**：独立运行的后台进程，从队列中消费任务并执行

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Monolith    │─────▶│ Message Queue │─────▶│ Async Worker │
│  (Web Server)│      │ (Redis/MQ)   │      │ (后台进程)    │
└──────────────┘      └──────────────┘      └──────────────┘
  同步处理请求           任务缓冲              异步处理耗时任务
```

关键特征：**代码仍然是一个代码库**（monolith），只是运行时拆成了两种进程角色（web + worker）。

## 为什么重要

单体应用处理 HTTP 请求时，遇到耗时操作会阻塞响应：

| 场景 | 同步处理的问题 |
|------|---------------|
| 发送邮件/短信 | 用户等 2-5 秒才收到响应 |
| 生成 PDF/报表 | 占用 Web 线程，影响并发 |
| 调用外部 API | 外部服务慢会拖垮整个应用 |
| 图片/视频处理 | CPU 密集，阻塞其他请求 |

加入 Async Worker 后，Web Server 只需把任务丢进队列立即返回，用户体验和系统吞吐量同时提升。

## 典型技术栈

| 语言/框架 | 队列 | Worker 框架 |
|-----------|------|-------------|
| Python / Django | Redis | **Celery** |
| Ruby / Rails | Redis | **Sidekiq** |
| Node.js / Express | Redis | **BullMQ** |
| Java / Spring | RabbitMQ / Kafka | **Spring AMQP** |
| Go | NATS / Redis | 自建 goroutine consumer |

## 架构演进中的位置

```
纯单体 ──▶ Monolith + Async Worker ──▶ 拆分微服务
  │                  │                       │
  同步阻塞           计算分离，代码仍一体      服务独立部署
```

这是单体向微服务演进的**第一步**——还没有拆服务，但已经把计算从请求路径中分离。很多中小型项目停留在这个阶段就足够了。

## 何时够用，何时该演进

**停留在此阶段的信号：**
- 团队 < 10 人，单一代码库管理方便
- Worker 任务类型 < 5 种，复杂度可控
- 部署频率不高，整体发布可接受

**需要继续演进的信号：**
- Worker 逻辑越来越重，需要独立扩缩容
- 不同 Worker 有不同的资源需求（CPU-bound vs IO-bound）
- 团队需要独立部署不同业务模块

## 相关概念

- [[message-queue|消息队列]] — Async Worker 的核心基础设施
- [[design-patterns|设计模式]] — Worker 中常用策略模式、命令模式
