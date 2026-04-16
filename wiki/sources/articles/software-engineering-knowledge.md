---
title: 软件工程知识资料
type: source
subtype: article
tags: [software-engineering, clean-code, design-patterns, refactoring, solid, ddd]
created: 2026-04-16
updated: 2026-04-16
sources:
  - ../../raw/articles/software-engineering-knowledge.md
---

# 软件工程知识资料

> 整理自 AI 助手使用 gh search 检索的优质软件工程知识资源，覆盖代码质量、重构、设计模式、架构等核心领域。

## 核心资源概览

### 经典书籍

| 书名 | 作者 | 核心理念 |
|------|------|----------|
| 《代码大全》 | Steve McConnell | 软件构建百科全书 |
| 《重构》 | Martin Fowler | 代码坏味道+重构手法 |
| 《代码整洁之道》 | Robert C. Martin | SOLID原则+编码规范 |
| 《人月神话》 | Frederick Brooks | 软件项目管理经典 |
| 《架构整洁之道》 | Robert C. Martin | Clean Architecture |
| 《设计模式》 | GoF | 23种经典设计模式 |
| 《Effective Java》 | Joshua Bloch | Java高效实践 |

### 代码质量工具

- **SonarQube** — 静态代码分析平台
- **ESLint / Prettier** — JS/TS 规范+格式化
- **DeepSource** — 自动化代码审查
- **Codacy** — 云端代码质量分析
- **pre-commit** — 多语言 pre-commit 钩子框架

### 重构工具

- **ast-grep** — Rust 写的代码结构搜索/Lint/重写
- **rectorphp/rector** — PHP 自动升级和重构
- **Refactoring.Guru** — 设计模式+重构可视化

## 设计模式资源

### GoF 23种模式

创建型5种：Singleton、Factory Method、Abstract Factory、Builder、Prototype
结构型7种：Adapter、Bridge、Composite、Decorator、Facade、Flyweight、Proxy
行为型11种：Chain of Responsibility、Command、Iterator、Mediator、Memento、Observer、State、Strategy、Template Method、Visitor

### 多语言实现仓库

- [iluwatar/java-design-patterns](https://github.com/iluwatar/java-design-patterns) — Java 实现 ⭐
- [faif/python-patterns](https://github.com/faif/python-patterns) — Python 实现
- [tmrts/go-patterns](https://github.com/tmrts/go-patterns) — Go 实现
- [ochococo/Design-Patterns-In-Swift](https://github.com/ochococo/Design-Patterns-In-Swift) — Swift 实现
- [DesignPatternsPHP/DesignPatternsPHP](https://github.com/DesignPatternsPHP/DesignPatternsPHP) — PHP 8.x 实现
- [rust-unofficial/patterns](https://github.com/rust-unofficial/patterns) — Rust 反模式

### Clean Code 系列

- [ryanmcdermott/clean-code-javascript](https://github.com/ryanmcdermott/clean-code-javascript) — JS 版整洁代码 ⭐94k
- [labs42io/clean-code-typescript](https://github.com/labs42io/clean-code-typescript) — TypeScript 版
- [zedr/clean-code-python](https://github.com/zedr/clean-code-python) — Python 版

### SOLID 原则

五原则：S(单一职责)、O(开闭)、L(里氏替换)、I(接口隔离)、D(依赖倒置)

- [heykarimoff/solid.python](https://github.com/heykarimoff/solid.python) — Python SOLID
- [bespoyasov/solidbook](https://github.com/bespoyasov/solidbook) — SOLID 原则书籍

### 架构模式

- [rmanguinho/clean-ts-api](https://github.com/rmanguinho/clean-ts-api) — TDD+Clean+SOLID
- [heynickc/awesome-ddd](https://github.com/heynickc/awesome-ddd) — DDD+CQRS+EventSourcing 资源

### 反模式

- [rust-unofficial/patterns](https://github.com/rust-unofficial/patterns) — Rust 反模式
- [quantifiedcode/python-anti-patterns](https://github.com/quantifiedcode/python-anti-patterns) — Python 反模式
- [tcorral/Refactoring_Patterns](https://github.com/tcorral/Refactoring_Patterns) — 31种 JS 重构模式

## 学习路线

```
1. 入门：读《代码整洁之道》 + clean-code-javascript
2. 实践：用 ESLint + Prettier 规范团队代码
3. 进阶：学 SonarQube + 理解《重构》23种坏味道
4. 体系化：掌握 SOLID / DRY / KISS 原则 + DDD
```

## 实用链接

- [Refactoring.Guru](https://refactoringguru.cn/) — 设计模式+重构可视化
- [Sourcemaking](https://sourcemaking.com/) — 设计模式与重构
- [Kamran Ahmed - Design Patterns for Humans](https://github.com/kamranahmedse/design-patterns-for-humans) ⭐70k
- [Teach Yourself CS](https://teachyourselfcs.com/) — 自学计算机科学
- [System Design Primer](https://github.com/donnemartin/system-design-primer) ⭐150k

## 相关概念

- [[clean-code|Clean Code]] — 整洁代码原则
- [[design-patterns|设计模式]] — GoF 23种模式
- [[solid-principles|SOLID 原则]] — 面向对象设计五原则
- [[refactoring|重构]] — 改善既有代码设计
