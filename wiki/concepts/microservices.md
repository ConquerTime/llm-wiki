---
title: 微服务架构
type: concept
subtype: programming
tags: [programming, microservices, distributed-systems, architecture]
created: 2026-04-16
updated: 2026-04-16
sources:
  - ../sources/articles/backend-architecture-article.md
---

# 微服务架构

> 将单体应用拆分为多个独立可部署服务的设计风格。

## 核心理念

| 理念 | 说明 |
|------|------|
| **单一职责** | 每个服务只负责一个业务领域 |
| **独立部署** | 服务间无直接依赖，可独立发布 |
| **去中心化** | 每个服务自主选择技术栈 |
| **故障隔离** | 一个服务故障不导致全局崩溃 |

## 服务间通信

### 同步通信

- **REST / HTTP** — 最常用
- **gRPC** — 高性能二进制协议
- **GraphQL** — 客户端驱动查询

### 异步通信

- **消息队列** — RabbitMQ / Kafka / Redis Streams
- **事件总线** — 发布/订阅模式

## API Gateway

所有客户端的统一入口：

```
Client → API Gateway → Auth → Rate Limit → Routes → Services
                            ↓
                    聚合/路由/协议转换
```

功能：路由、认证、限流、监控、协议转换

## 服务发现

| 方案 | 工具 |
|------|------|
| **客户端发现** | Eureka, Consul (client-side) |
| **服务端发现** | Nginx, Envoy (server-side) |

## 分布式数据管理

| 问题 | 解决方案 |
|------|----------|
| **跨服务查询** | API 组合 / CQRS Read Model |
| **分布式事务** | Saga 模式 / 最终一致性 |
| **数据一致性** | Event Sourcing |

## Saga 模式

将分布式事务拆分为一系列局部事务 + 补偿操作：

```
Order Service → Payment Service → Inventory Service
    ↓ compensate      ↓ compensate      ↓
   cancel order      refund           restore stock
```

两种实现：
- **Choreography** — 服务间通过事件协调
- **Orchestration** — 中央编排器控制流程

## 相关资源

- [mfornos/awesome-microservices](https://github.com/mfornos/awesome-microservices) — 微服务资源合集
- [jhipster/generator-jhipster](https://github.com/jhipster/generator-jhipster) — 微服务生成平台
- [mehdihadeli/go-food-delivery-microservices](https://github.com/mehdihadeli/go-food-delivery-microservices) — Go 微服务完整示例

## 相关概念

- [[backend-architecture|后端架构]] — 核心架构模式
- [[cloud-deployment|云服务部署]] — 部署与运维
