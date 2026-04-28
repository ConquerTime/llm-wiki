---
title: 整洁代码
type: concept
subtype: programming
tags: [programming, clean-code, solid]
created: 2026-04-16
updated: 2026-04-16
sources:
  - ../sources/articles/software-engineering-knowledge.md
---

# 整洁代码

> 编写代码时追求的一种状态：代码清晰、意图明确、易于维护。

## 核心理念

整洁代码的核心原则来自 Robert C. Martin（Uncle Bob）的《代码整洁之道》：

### SOLID 原则

| 原则 | 全称 | 说明 |
|------|------|------|
| S | Single Responsibility | 单一职责：每个类只做一件事 |
| O | Open/Closed | 开闭原则：对扩展开放，对修改封闭 |
| L | Liskov Substitution | 里氏替换：子类必须能替换基类 |
| I | Interface Segregation | 接口隔离：接口要小而专 |
| D | Dependency Inversion | 依赖倒置：依赖抽象而非具体 |

### 其他关键原则

- **DRY** — Don't Repeat Yourself，不重复自己
- **KISS** — Keep It Simple, Stupid，保持简单
- **YAGNI** — You Aren't Gonna Need It，不做过度设计

## 多语言整洁代码指南

| 仓库 | 语言 | ⭐ |
|------|------|-----|
| [ryanmcdermott/clean-code-javascript](https://github.com/ryanmcdermott/clean-code-javascript) | JavaScript | 94k |
| [labs42io/clean-code-typescript](https://github.com/labs42io/clean-code-typescript) | TypeScript | 🔥 |
| [zedr/clean-code-python](https://github.com/zedr/clean-code-python) | Python | 🔥 |
| [piotrplenik/clean-code-php](https://github.com/piotrplenik/clean-code-php) | PHP | 🔥 |
| [thangchung/clean-code-dotnet](https://github.com/thangchung/clean-code-dotnet) | .NET | 🔥 |

## 代码质量工具

### 静态分析

- **SonarQube** — 综合性代码质量平台
- **ESLint / Prettier** — JS/TS 代码规范+格式化
- **DeepSource** — 自动化代码审查
- **Codacy** — 云端代码质量分析

### pre-commit 钩子

- [pre-commit/pre-commit](https://github.com/pre-commit/pre-commit) — 多语言 pre-commit 框架 ⭐

## 实用链接

- [Refactoring.Guru](https://refactoringguru.cn/) — 重构与设计模式可视化
- [Sourcemaking](https://sourcemaking.com/) — 设计模式与重构

## 相关概念

- [[design-patterns|设计模式]] — GoF 23种模式
- [[solid-principles|SOLID 原则]] — 面向对象设计五原则
- [[refactoring|重构]] — 改善既有代码设计
- [[factory-method|工厂方法]] — SOLID 原则中"开闭原则"的典型应用场景
