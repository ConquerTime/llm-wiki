---
title: SOLID 原则
type: concept
subtype: programming
tags: [solid, oop, design-principles, clean-code]
created: 2026-04-16
updated: 2026-04-16
sources:
  - ../sources/articles/software-engineering-knowledge.md
---

# SOLID 原则

> Robert C. Martin 提出的面向对象设计的五个基本原则，是 Clean Architecture 的基石。

## 五大原则

### S — 单一职责原则 (Single Responsibility Principle)

> 一个类只应该有一个改变的理由。

一个类只负责一件事，职责单一。当需求变化时，只有一个原因会导致这个类需要修改。

### O — 开闭原则 (Open/Closed Principle)

> 对扩展开放，对修改封闭。

软件实体应该对扩展开放，对修改关闭。可以通过继承、多态等机制来扩展行为，而不是修改现有代码。

### L — 里氏替换原则 (Liskov Substitution Principle)

> 子类必须能够替换其基类。

任何基类出现的地方，子类都可以替换它，而不影响程序的正确性。这意味着子类不能改变父类行为的前置条件或后置条件。

### I — 接口隔离原则 (Interface Segregation Principle)

> 客户端不应该依赖它不需要的接口。

将臃肿的接口拆分成更小、更具体的接口，让类只依赖它实际需要的方法。

### D — 依赖倒置原则 (Dependency Inversion Principle)

> 高层模块不应该依赖低层模块，两者都应该依赖抽象。

依赖抽象而不是具体实现。抽象接口不应该依赖具体实现，具体实现应该依赖抽象接口。

## 学习资源

| 仓库 | 描述 | ⭐ |
|------|------|-----|
| [heykarimoff/solid.python](https://github.com/heykarimoff/solid.python) | Python 理解 SOLID | 🔥 |
| [bespoyasov/solidbook](https://github.com/bespoyasov/solidbook) | SOLID 原则书籍 | 🔥 |
| [jafari-dev/oop-expert-with-typescript](https://github.com/jafari-dev/oop-expert-with-typescript) | TS 面向对象+SOLID | 🔥 |

## Clean Architecture + SOLID

| 仓库 | 描述 | ⭐ |
|------|------|-----|
| [rmanguinho/clean-ts-api](https://github.com/rmanguinho/clean-ts-api) | TDD+Clean+SOLID 完整示例 | 🔥 |
| [rmanguinho/clean-react](https://github.com/rmanguinho/clean-react) | React+Clean Architecture | 🔥 |
| [qiangxue/go-rest-api](https://github.com/qiangxue/go-rest-api) | Go REST API+SOLID | 🔥 |

## 相关概念

- [[clean-code|Clean Code]] — 整洁代码原则
- [[design-patterns|设计模式]] — GoF 23种模式
- [[refactoring|重构]] — 改善既有代码设计
- [[factory-method|工厂方法]] — 开闭原则的典型实现，通过工厂方法而非修改创建者代码来引入新产品
