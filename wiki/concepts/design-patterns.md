---
title: 设计模式
type: concept
subtype: programming
tags: [programming, design-patterns, clean-code]
created: 2026-04-16
updated: 2026-04-16
sources:
  - ../sources/articles/software-engineering-knowledge.md
  - ../sources/articles/observer-pattern.md
---

# 设计模式

> 总结实践中反复出现的通用问题的通用可复用解决方案。

## 概述

设计模式是软件设计中常见问题的通用、可复用的解决方案。由 GoF（四人组）于 1994 年在《设计模式》一书中系统化提出。

## GoF 23种设计模式

### 创建型模式（5种）

解决对象创建问题

| 模式 | 目的 |
|------|------|
| Singleton | 确保一个类只有一个实例 |
| Factory Method | 定义创建对象的接口，让子类决定实例化哪个类 |
| Abstract Factory | 创建一系列相关对象的接口 |
| Builder | 分离复杂对象的构建和表示 |
| Prototype | 通过拷贝原型对象来创建新对象 |

### 结构型模式（7种）

处理对象组合

| 模式 | 目的 |
|------|------|
| Adapter | 将一个类的接口转换成客户希望的另一个接口 |
| Bridge | 将抽象部分与实现部分分离，使它们可以独立变化 |
| Composite | 将对象组合成树形结构以表示"部分-整体"层次结构 |
| Decorator | 动态地给对象添加额外的职责 |
| Facade | 为子系统中一组接口提供一个统一的接口 |
| Flyweight | 运用共享技术有效地支持大量细粒度对象 |
| Proxy | 为其他对象提供一种代理以控制对这个对象的访问 |

### 行为型模式（11种）

处理对象间的通信

| 模式 | 目的 |
|------|------|
| Chain of Responsibility | 将请求的发送者和接收者解耦 |
| Command | 将请求封装成对象 |
| Iterator | 提供一种方法顺序访问集合元素而不暴露底层表示 |
| Mediator | 用一个中介对象来封装一系列对象交互 |
| Memento | 在不破坏封装性的前提下捕获对象内部状态 |
| [[programming/observer-pattern\|Observer]] | 定义对象间的一种一对多依赖关系，发布者状态变化自动通知所有订阅者 |
| State | 允许对象在其内部状态改变时改变行为 |
| Strategy | 定义一系列算法，把它们一个个封装起来 |
| Template Method | 定义算法骨架，将一些步骤延迟到子类 |
| Visitor | 表示一个作用于某对象结构中的各元素的操作 |

## 多语言实现

| 仓库 | 语言 | ⭐ |
|------|------|-----|
| [iluwatar/java-design-patterns](https://github.com/iluwatar/java-design-patterns) | Java | 🔥 |
| [faif/python-patterns](https://github.com/faif/python-patterns) | Python | 🔥 |
| [tmrts/go-patterns](https://github.com/tmrts/go-patterns) | Go | 🔥 |
| [rust-unofficial/patterns](https://github.com/rust-unofficial/patterns) | Rust | 🔥 |
| [fbeline/design-patterns-JS](https://github.com/fbeline/design-patterns-JS) | JavaScript | 🔥 |

## 学习资源

- [Kamran Ahmed - Design Patterns for Humans](https://github.com/kamranahmedse/design-patterns-for-humans) — 极简版解释 ⭐70k
- [Refactoring.Guru](https://refactoringguru.cn/) — 可视化学习
- [Sourcemaking](https://sourcemaking.com/) — 设计模式与重构

## 相关概念

- [[clean-code|Clean Code]] — 整洁代码原则
- [[solid-principles|SOLID 原则]] — 面向对象设计五原则
- [[refactoring|重构]] — 改善既有代码设计
- [[unified-payment-route|统一支付路由]] — 设计模式在实际业务系统（电商支付）中的应用案例
- [[backend-architecture|后端架构]] — 设计模式在后端系统分层、微服务、CQRS 等架构中的综合应用
