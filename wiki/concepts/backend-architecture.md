---
title: 后端架构
type: concept
subtype: programming
tags: [backend, architecture, microservices, cloud, devops]
created: 2026-04-16
updated: 2026-04-16
sources:
  - ../sources/articles/backend-architecture.md
---

# 后端架构

> 服务端系统的整体结构设计与技术选型。

## 核心架构模式

### 分层架构 (Layered Architecture)

最经典的后端架构，按职责分为多层：

```
Controller → Service → Repository
     ↓          ↓          ↓
  请求处理   业务逻辑   数据访问
```

适合：传统 Web 应用、CRUD 系统

### 六边形架构 (Hexagonal Architecture)

核心业务逻辑与外部依赖完全解耦，通过"端口"和"适配器"连接：

```
        外部世界
           ↓
    ┌─────────────┐
    │   适配器     │ ←→  ports (接口)
    └─────────────┘
           ↓
    ┌─────────────┐
    │  核心业务    │ ← domain model
    └─────────────┘
           ↓
    ┌─────────────┐
    │   适配器     │ ←→  ports (接口)
    └─────────────┘
           ↓
        外部世界
```

适合：需要高度可测试性和框架无关性的系统

### Clean Architecture

Robert C. Martin 提出的同心圆架构：

```
  外圈：框架/驱动
    ↓
  外圈：接口适配器
    ↓
  内圈：业务规则
    ↓
  核心：实体
```

依赖方向：外圈依赖内圈，内圈不关心外圈实现

### CQRS (Command Query Responsibility Segregation)

读写分离：同一个 domain 使用不同的 model

- **Command** — 修改操作，返回 void 或 ID
- **Query** — 读取操作，返回 DTO

配合 Event Sourcing 实现复杂业务场景。

## 扩展阅读

- [afteracademy/nodejs-backend-architecture-typescript](https://github.com/afteracademy/nodejs-backend-architecture-typescript)
- [TFdream/awesome-backend-architecture](https://github.com/TFdream/awesome-backend-architecture)

## 相关概念

- [[design-patterns|设计模式]] — 软件设计模式
- [[clean-code|Clean Code]] — 整洁代码原则
