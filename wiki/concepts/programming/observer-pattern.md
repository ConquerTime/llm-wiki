---
title: 观察者模式（Observer）
type: concept
subtype: programming
tags: [design-patterns, observer, behavioral, gof, event, pub-sub]
created: 2026-04-17
updated: 2026-04-17
sources:
  - ../../sources/articles/observer-pattern.md
---

# 观察者模式（Observer）

> 行为型设计模式：定义对象间一对多依赖关系，发布者状态变化时自动通知所有订阅者，且双方通过接口解耦。

## 核心思想

将"谁需要知道变化"的逻辑从发布者中抽离出去，由订阅者自行注册兴趣。发布者只负责在变化时广播通知，不需要知道谁在听、有多少人在听。

## 三个关键设计决策

1. **统一接口** — 所有订阅者实现同一个 `Subscriber` 接口（含 `update` 方法），发布者仅依赖接口不耦合具体类
2. **动态订阅列表** — 运行时可随时 subscribe/unsubscribe，订阅关系不在编译期确定
3. **委派 EventManager** — 发布者可将订阅列表管理委派给帮手对象，使发布者专注业务逻辑

## 伪代码骨架

```
// 发布者
class EventManager:
    listeners: Map<eventType, List<Listener>>

    subscribe(type, listener)
    unsubscribe(type, listener)
    notify(type, data):
        for each listener in listeners[type]:
            listener.update(data)

// 订阅者接口
interface EventListener:
    update(data)

// 具体发布者委派给 EventManager
class Editor:
    events: EventManager
    openFile(path):
        events.notify("open", path)
```

## 适用场景

- 对象状态变更需通知一批未知的其他对象（数量、类型事先不知道）
- GUI 按钮/控件需支持外部注入响应逻辑
- 需要在运行时动态建立/解除对象间联系

## 与相似模式的区别

| 模式 | 区别 |
|------|------|
| [[mediator|Mediator（中介者）]] | Mediator 消除多对多依赖（双向），Observer 建立一对多单向通知 |
| Pub/Sub | Observer 订阅者直接引用发布者；Pub/Sub 通常通过消息中间件解耦，发布者和订阅者完全不认识彼此 |
| [[chain-of-responsibility|责任链]] | 责任链只有一个接收者处理请求；Observer 通知所有订阅者 |

## 来源

- [[../../sources/articles/observer-pattern|观察者模式 — Refactoring.Guru]] — 完整结构解析与伪代码
- [[../../concepts/design-patterns|设计模式]] — GoF 行为型模式分类
