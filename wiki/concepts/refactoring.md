---
title: 重构
type: concept
subtype: programming
tags: [refactoring, code-quality, design-patterns, technical-debt]
created: 2026-04-16
updated: 2026-04-16
sources:
  - ../sources/articles/software-engineering-knowledge.md
---

# 重构

> 在不改变代码外在行为的前提下，对代码内部结构进行调整，提高其可理解性和可修改性。

## 经典著作

- **《重构》** — Martin Fowler，系统阐述重构理论与实践

## 代码坏味道（Code Smells）

Fowler 在《重构》中列举了 23 种代码坏味道：

重复代码、过长函数、过大家庭、过长参数列表、依恋恋物、Data Clumps、Switch 惊悚、平行继承体系、冗余类、纯稚数据类型、异曲同工的类、令人迷惑的暂时变量、夸夸其谈的未来性...

## 常用重构工具

| 工具 | 语言 | 用途 |
|------|------|------|
| [ast-grep](https://github.com/ast-grep/ast-grep) | 多语言 | 代码结构搜索/Lint/重写 |
| [rectorphp/rector](https://github.com/rectorphp/rector) | PHP | 自动升级和重构 |
| [Refactoring.Guru](https://refactoringguru.cn/) | — | 可视化重构学习 |

## 重构模式

| 仓库 | 描述 |
|------|------|
| [tcorral/Refactoring_Patterns](https://github.com/tcorral/Refactoring_Patterns) | 31 种 JS 重构模式 |
| [KarlPurk/javascript-refactoring](https://github.com/KarlPurk/javascript-refactoring) | JS 重构模式收集 |

## 技术债务

重构常与偿还技术债务相关：

- [labcodes/awesome-technical-debt](https://github.com/labcodes/awesome-technical-debt) — 技术债务文章/书籍合集
- [lucidarch/lucid](https://github.com/lucidarch/lucid) — Laravel 最小化技术债务架构

## 实用链接

- [Refactoring.Guru](https://refactoringguru.cn/) — 重构与设计模式可视化
- [Sourcemaking](https://sourcemaking.com/) — 设计模式与重构

## 相关概念

- [[clean-code|Clean Code]] — 整洁代码原则
- [[design-patterns|设计模式]] — GoF 23种模式
- [[solid-principles|SOLID 原则]] — 面向对象设计五原则
