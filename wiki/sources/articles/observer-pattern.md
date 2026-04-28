---
title: 观察者模式 — Refactoring.Guru
type: source
subtype: article
tags: [programming, design-patterns]
created: 2026-04-17
updated: 2026-04-17
sources:
  - ../../../raw/观察者.md
author: Refactoring.Guru
url: https://refactoringguru.cn/design-patterns/observer
date: 2025-01
---

# 观察者模式 — Refactoring.Guru

> Refactoring.Guru 对 GoF 观察者（Observer）模式的系统性讲解：意图、结构、伪代码、适用场景、优缺点及与相关模式的对比。

## 核心摘要

观察者是一种行为型设计模式，通过订阅机制让**发布者**在状态变化时自动通知所有**订阅者**，实现一对多依赖，且发布者不需要了解订阅者的具体类型。

## 关键要点

- **核心矛盾**：订阅者主动轮询（浪费时间）vs 发布者向所有人广播（浪费资源）；观察者模式通过订阅机制解决此矛盾
- **机制要素**：① 存储订阅者引用的列表；② 添加/删除订阅者的公有方法；③ 遍历列表触发通知的 `notify` 方法
- **接口解耦**：所有订阅者必须实现同一接口（含 `update` 方法），发布者仅依赖接口，不耦合具体类
- **委派模式**：发布者可将订阅列表管理委派给专门的 EventManager 帮手对象，实现更灵活的事件分发
- **适用场景**：① 对象状态变化需通知其他未知对象；② 图形界面按钮注入自定义响应代码；③ 订阅关系需在运行时动态建立和销毁

## 结构角色

| 角色 | 职责 |
|------|------|
| Publisher（发布者） | 维护订阅列表，状态变化时触发 notify |
| Subscriber 接口 | 声明 `update` 方法，统一所有订阅者契约 |
| Concrete Subscriber | 实现 `update`，执行业务响应逻辑 |
| Client | 创建发布者和订阅者，完成注册 |

## 关键引文

> "所有订阅者都必须实现同样的接口，发布者仅通过该接口与订阅者交互。"

> "订阅列表是动态生成的：对象可在运行时根据程序需要开始或停止监听通知。"

## 优缺点

**优点**
- 开闭原则：无需修改发布者即可引入新订阅者
- 运行时动态建立对象间联系

**缺点**
- 订阅者通知顺序随机，无法保证顺序

## 与相关模式的区别

| 对比 | 说明 |
|------|------|
| Observer vs Mediator | Mediator 目标是消除多组件间相互依赖，Observer 目标是建立动态单向连接 |
| Observer vs Chain of Responsibility | 责任链按顺序传递直到被处理；Observer 通知所有订阅者 |
| Observer vs Command | Command 建立发送者到请求者的单向连接；Observer 允许动态订阅/取消 |

## 提到的概念

- [[../../../wiki/concepts/design-patterns|设计模式]] — GoF 23种模式
- [[observer|观察者模式]] — 本页主题
