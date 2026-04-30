---
title: 后端架构栈
type: synthesis
tags: [programming, backend, architecture]
created: 2026-04-28
updated: 2026-04-28
sources:
  - "[[wiki/sources/articles/backend-architecture-article.md|后端架构知识资料]]"
---

# 后端架构栈

> 后端的"架构"不是单一维度的选择题，而是六层叠起来的栈：**拓扑形态 → 内部结构 → 数据与异步 → 一致性与正确性 → 部署与发布 → 可观测与安全**。本页把 wiki 里散落的后端相关页面组装成这张栈图，给出"遇到 X 问题时，看哪一层的哪个页面"的统一视角。

## 为什么需要"栈"这个视角

后端架构的讨论常陷入两极：

- **一极**：只讨论"要不要上微服务" —— 把拓扑当全部
- **另一极**：只讨论"选哪个队列" —— 只看单点技术

真正的坑出现在**层与层之间的耦合**：
- 拓扑选了微服务，但内部架构还是贫血 Controller→Service→Repository，拆出的服务本质是"远程的 CRUD"，没解决任何问题
- 异步层引入了消息队列，但没做 Outbox 和幂等，上线后开始丢消息 / 重复处理
- 部署上了金丝雀，但数据库 Schema 不向后兼容，金丝雀期间老版本直接崩
- 读写分离配好了，但业务代码没考虑写后读一致性，用户发帖后刷新看不到自己的帖子

这些坑**单独看任何一页都无法预防**——必须把整栈拉通来看。

```
┌─────────────────────────────────────────┐
│  L5 — 可观测性与安全                      │  ← Metrics / Logs / Traces，认证授权
├─────────────────────────────────────────┤
│  L4 — 部署与发布                         │  ← 云平台 / IaC / CI-CD / 金丝雀
├─────────────────────────────────────────┤
│  L3 — 一致性与正确性                     │  ← 写后读 / Saga / 幂等 / SKIP LOCKED
├─────────────────────────────────────────┤
│  L2 — 数据与异步                         │  ← 消息队列 / Outbox / 步骤缓存
├─────────────────────────────────────────┤
│  L1 — 内部结构                           │  ← 分层 / 六边形 / Clean / CQRS
├─────────────────────────────────────────┤
│  L0 — 拓扑形态                           │  ← Monolith → +Worker → 微服务
└─────────────────────────────────────────┘
```

## L0 — 拓扑形态（Topology）

**问题**：系统由几个进程、几个代码库、几个部署单元组成？

**演进路径**：

```
纯 Monolith ──▶ Monolith + Async Worker ──▶ 微服务
   │                     │                      │
 单进程同步            代码库单体                服务独立部署
                      运行时分两种进程           跨服务通信 + Saga
```

**判断标准**：

| 信号 | 推荐形态 |
|------|---------|
| 团队 < 5 人，业务模型尚未稳定 | 纯 Monolith |
| 出现长耗时任务（邮件 / PDF / AI 生成 / 外部 API） | + Async Worker |
| 不同 Worker 有不同资源需求（CPU vs IO） | 拆独立 Worker 服务 |
| 团队 > 10 人，多个业务域需要独立发布节奏 | 微服务 |
| 需要跨技术栈（Python 模型 + Node API） | 微服务 |

**关联**：[[wiki/concepts/programming/monolith-async-worker.md|Monolith with Async Worker]] · [[wiki/concepts/microservices.md|微服务架构]]

**常见错误**：**过早拆微服务**。业务模型没稳定就按"领域"拆服务，拆完发现边界画错，跨服务调用漫天飞——这时调整边界的代价比单体内部重构高一个数量级。口诀：**Monolith First**。

## L1 — 内部结构（Internal Architecture）

**问题**：单个服务内部怎么组织代码？控制器、业务、数据、外部依赖各住哪？

**四种经典模式**：

| 模式 | 核心思想 | 适合 |
|------|---------|------|
| **Layered**（分层） | Controller → Service → Repository 线性依赖 | 传统 CRUD / 中小型系统 |
| **Hexagonal**（六边形） | 核心业务通过 port/adapter 连外部依赖 | 高测试性要求 / 多适配器 |
| **Clean Architecture** | 同心圆，外圈依赖内圈，内圈不知外圈 | 复杂业务 / 长生命周期 |
| **CQRS** | 读写分离，Command 与 Query 用不同 model | 读远多于写 / 复杂查询 |

**关联**：[[wiki/concepts/backend-architecture.md|后端架构]]

**L0 vs L1 的关系**：拓扑不能替代内部架构。
- 单体里内部架构差 → 代码腐烂成泥球
- 微服务里内部架构差 → 每个服务都是远程的泥球，还多了网络抖动

反过来也成立：
- 内部架构好的单体可以走很久（Basecamp / Shopify）
- 内部架构好的服务才有"可拆性"（Clean Architecture 的"插拔外圈"天然便于拆服务）

**常见错误**：
- **贫血模型**：Service 层只是 Controller 和 Repository 的胶水，真正的业务逻辑散在 Controller 或 Repository 里
- **Clean Architecture 过度设计**：简单 CRUD 硬套 Entity / UseCase / Interactor / Presenter 四层，写 10 个文件做一件事
- **CQRS 无读压力硬上**：读写一个数量级时上 CQRS，只是给自己挖坑

## L2 — 数据与异步（Data & Async）

**问题**：耗时任务怎么卸载？跨进程消息怎么传？数据库 + 消息队列的双写怎么保证一致？

**核心工具**：

| 主题 | 工具 / 模式 |
|------|------------|
| 异步任务 | 消息队列（Redis/BullMQ、RabbitMQ、Kafka） |
| 事务性消息 | **Outbox Pattern**（业务表 + Outbox 表同一事务） |
| 幂等消费 | jobId 去重 / processed_events 表 / 步骤缓存 |
| 重试策略 | 指数退避 + 最大次数 + 死信队列 |
| 补偿扫描 | Poller + `SELECT FOR UPDATE SKIP LOCKED` |
| 定时任务 | Repeatable Job（固定 jobId 防重） |

**关联**：[[wiki/concepts/programming/message-queue.md|消息队列]]

**关键洞见 —— Outbox 是"跨资源一致性"的通解**：

```
事务内：                    事务外（best-effort）：
  INSERT business_data        publishEvent(eventId)
  INSERT domain_events        ↓ 失败？Poller 30s 后补偿
  (status='pending')
  COMMIT
```

Outbox 的本质是**把"数据库写 + 消息发"合并成单一事务**——DB 写入保证原子，消息发送转为最终保证（Poller 兜底）。这个模式一旦理解，"双写不一致"这一整类问题都迎刃而解（不只是 DB + MQ，DB + 外部 API、DB + 缓存都可用）。

**常见错误**：
- **先发消息再写 DB**：消息发出去了，DB 回滚，消费者看到"幽灵消息"
- **先写 DB 再发消息，无 Outbox**：DB 成功、网络抖动导致消息丢失——没有任何机制补偿
- **有 Outbox 没 Poller**：遇到 Redis/MQ 宕机窗口就丢消息
- **多 Poller 没 SKIP LOCKED**：水平扩容后同一事件被处理多次

## L3 — 一致性与正确性（Correctness）

**问题**：分布式系统里"数据对不对"的那一类陷阱——不是功能 bug，是**物理意义上的时间差**带来的错乱。

**三类核心问题**：

### 3.1 写后读（Read-After-Write）

用户刚写，立刻读——结果读不到（主从复制延迟）。

**解法**：
- 写完读主节点（用户读自己数据的场景最简）
- 时间戳路由（有读扩展需求）
- Session Sticky（无状态服务最简）
- 同步复制（金融场景，牺牲写延迟）
- 客户端乐观更新（前端 React Query / SWR 的 `mutate`）

**关联**：[[wiki/concepts/programming/read-after-write.md|写后读问题]]

### 3.2 幂等消费（Idempotency）

同一条消息被处理多次，结果必须与一次相同。见 L2 的 `processed_events` 表 + `jobId` 去重。

### 3.3 分布式事务（Saga）

跨服务操作要么都成功要么都回滚——但分布式没有 XA 可用，用 Saga 拆成"局部事务 + 补偿操作"：

- **Choreography**：服务间通过事件自协调，去中心
- **Orchestration**：中央编排器控制流程，可观测性好

**关联**：[[wiki/concepts/microservices.md|微服务架构]]（Saga 章节）

**L2 vs L3 的关系**：L2 是**工具与模式**（队列、Outbox），L3 是**正确性保证**（一致性、幂等、事务）。选对了 L2 工具，L3 的保证才有落点；选错了 L2（比如用 Redis List 当队列，无 ACK 语义），L3 的正确性根本无从谈起。

## L4 — 部署与发布（Deployment & Release）

**问题**：代码怎么从 `git push` 到生产？怎么在不停机的前提下换版本？

**核心概念**：

| 主题 | 工具 |
|------|------|
| 容器化 | Docker / Dockerfile / Registry |
| 编排 | Kubernetes（Pod/Deployment/Service/Ingress）/ Cloud Run |
| IaC | Terraform / AWS CDK / Azure Bicep / Pulumi |
| CI/CD | GitHub Actions / GitLab CI / ArgoCD |
| 发布策略 | 全量 / 蓝绿 / **金丝雀** / 滚动更新 / Feature Flag |

**关联**：[[wiki/concepts/cloud-deployment.md|云服务部署]] · [[wiki/concepts/programming/canary-deployment.md|金丝雀部署]]

**发布策略对比**：

| 策略 | 风险 | 回滚速度 | 适合 |
|------|------|---------|------|
| 全量发布 | 高 | 慢 | 小应用 / 内部系统 |
| 蓝绿 | 中 | 快（切环境） | 对状态切换不敏感的服务 |
| **金丝雀** | **低** | **快（缩流量）** | **生产服务默认选择** |
| Feature Flag | 低 | 即时 | 配合金丝雀使用效果最好 |

**L4 vs L3 的耦合陷阱 —— Schema 变更与金丝雀的死亡组合**：

金丝雀期间新旧版本并存。如果新版本做了不向后兼容的 Schema 变更（删列、改类型），老版本实例立刻崩溃——金丝雀的"只影响少数用户"变成"大多数用户先崩"。

解法：**Expand-Contract 模式**

```
Phase 1（发布前）：添加新列，不删旧列 → 新旧版本都能运行
Phase 2（发布中）：金丝雀 5% → 25% → 50% → 100%
Phase 3（完成后）：删除旧列 / 老 API
```

这一步要跨 L1（代码支持双写）+ L3（数据迁移期间的一致性）+ L4（发布节奏），**三层协同**，任何一层掉链子都翻车。

## L5 — 可观测性与安全（Observability & Security）

**问题**：系统跑起来了，怎么知道它跑得对不对？出了事怎么追？

**可观测性三支柱**：

| 类型 | 工具 | 回答什么问题 |
|------|------|------------|
| **Metrics** | Prometheus / CloudWatch | "系统现在健康吗"（数值、趋势） |
| **Logs** | Loki / ELK / CloudWatch Logs | "这个请求发生了什么"（事件、堆栈） |
| **Traces** | Jaeger / Zipkin | "这次慢在哪里"（跨服务链路） |

统一标准：**OpenTelemetry**（metrics + logs + traces 统一规范，厂商中立）

**关联**：[[wiki/concepts/cloud-deployment.md|云服务部署]]（可观测性章节）

**L5 在整栈中的作用**：
- L0 拓扑越复杂，L5 投入越关键（单体出问题 tail 日志就能查；微服务出问题没有 Trace 根本找不到源头）
- L2 的消息队列天然是**黑盒**，没有 metrics（积压数、处理延迟、失败率）等于开黑箱在跑
- L3 的一致性问题通常**不报错**，只能靠监控（写入版本号 vs 读取版本号 mismatch 率）发现

**安全维度**（wiki 目前覆盖较浅，仅列主要切面）：
- **认证**：JWT / OAuth2 / Session
- **授权**：RBAC（粗粒度角色）+ PBAC（细粒度所有权）
- **传输**：TLS / mTLS（服务间）
- **密钥管理**：Vault / AWS Secrets Manager / SOPS

## 栈内典型问题的定位

几个具体问题，看看它们落在栈的哪一层：

| 症状 | 真正的层 | 治理方法 |
|------|---------|---------|
| "用户发帖后立刻刷新看不到自己帖子" | L3 写后读 | 读主节点 / 客户端乐观更新 |
| "支付成功但积分没加" | L2 双写一致性 | Outbox Pattern |
| "消息被消费了两次导致重复发邮件" | L3 幂等 | processed_events 表 |
| "微服务间数据对不上" | L3 Saga | Choreography / Orchestration |
| "上线后 500 错误率飙升" | L4 发布策略 | 上金丝雀，减小爆炸半径 |
| "金丝雀期间老版本崩了" | L1 + L4 | Expand-Contract Schema 演进 |
| "水平扩容后定时任务跑了 3 次" | L2 Repeatable Job | 固定 jobId 幂等注册 |
| "Poller 并发扫描导致同一事件被处理多次" | L2 并发控制 | SELECT FOR UPDATE SKIP LOCKED |
| "业务逻辑散在 Controller 和 Repository 里" | L1 贫血模型 | 提升到 Domain Service / Use Case |
| "服务拆得太细，跨服务调用漫天飞" | L0 拓扑错误 | 合并回小数量的粗粒度服务 |

**用法**：下次遇到一个后端问题，**先定位是哪一层的问题**，再在对应层找工具。跨层乱改（L3 问题用 L0 拓扑调整去修）是常见踩坑。

## 前后端栈的对位

后端栈和 [[wiki/synthesis/react-architecture-stack.md|React 架构栈]] 在思维上高度同构——都是**按维度分层 + 每层独立选工具**的分解。

| 维度 | 后端 | React 前端 |
|------|------|-----------|
| 项目组织 | L1 Layered / Hexagonal / Clean | L1 Feature-Based |
| 状态分层 | L1 CQRS（读写分离） | L2 状态五分类 |
| 数据层 | L2 消息队列 / Outbox | L3 Server Cache（TanStack Query） |
| 一致性 | L3 写后读 / Saga / 幂等 | L4 页面反模式（状态合并） |
| 部署 | L4 金丝雀 / IaC | L0 SPA fallback |
| 正确性纪律 | L5 可观测性 | L5 组件反模式 |

**共同底层**：[[wiki/concepts/solid-principles.md|SOLID]]（单一职责、依赖反转）、[[wiki/concepts/clean-code.md|DRY/KISS/YAGNI]]、[[wiki/concepts/refactoring.md|重构]]。

## 什么时候不需要完整栈

不是每个后端都要铺完这六层：

| 场景 | 最少栈 |
|------|-------|
| 个人项目 / MVP / 内部工具 | L0（单体）+ L1（分层）+ L4（全量发布）|
| 中小业务（5-20 人团队） | + L2（MQ + Outbox）+ L4（金丝雀）+ L5（基础 metrics） |
| 高并发 / 多区域 / 金融级 | 全栈 + L3 同步复制 + L5 完整 trace 链路 |

**升级信号**：
- 出现"长耗时操作阻塞响应"→ 补 L2 异步
- 出现"跨资源双写不一致"→ 补 L2 Outbox
- 出现"上线全量翻车"→ 补 L4 金丝雀
- 出现"跨服务数据对不上"→ 补 L3 Saga
- 出现"半夜线上报警没人知道为什么"→ 补 L5 可观测性

## 开放问题

- **Serverless（Lambda / Cloud Run）如何改写 L0 和 L4？** Serverless 让"拓扑 + 部署"两层合并——没有长驻进程、没有金丝雀实例的概念，取而代之的是版本别名 + 流量权重。L0/L4 的边界在重新绘制。
- **Event Sourcing + CQRS 会吞并 L1 和 L2 吗？** Event Sourcing 让"业务事件"本身就是数据源，事件流天然跨越 L1 内部架构和 L2 异步边界。但复杂度高、调试难，目前只在特定领域（金融交易、审计）稳定落地。
- **AI/Agent 服务的后端栈长什么样？** LLM 调用天然耗时（秒～分钟级）+ 高失败率，L2 异步 + L3 幂等成为**默认配置而非可选**。[[wiki/concepts/programming/message-queue.md|消息队列]]里的 kaigao 项目实践就是这类范式的实例。
- **Database per Service 真的是微服务铁律吗？** 严格执行会让 L3 一致性代价飙升（跨库查询、跨库事务都要走 Saga）。业界开始出现"共享数据库但强边界"的折衷（每个服务只读写自己 schema）。

## 相关页面

- **L0 拓扑**：[[wiki/concepts/programming/monolith-async-worker.md|Monolith with Async Worker]] · [[wiki/concepts/microservices.md|微服务架构]]
- **L1 内部**：[[wiki/concepts/backend-architecture.md|后端架构]]（Layered / Hexagonal / Clean / CQRS）
- **L2 数据/异步**：[[wiki/concepts/programming/message-queue.md|消息队列]]（BullMQ / Outbox / 幂等 / SKIP LOCKED）
- **L3 一致性**：[[wiki/concepts/programming/read-after-write.md|写后读问题]]
- **L4 部署**：[[wiki/concepts/cloud-deployment.md|云服务部署]] · [[wiki/concepts/programming/canary-deployment.md|金丝雀部署]]
- **跨层业务参考**：[[wiki/concepts/programming/unified-payment-route.md|统一支付路由设计]]（L1 内部结构 + L2 异步 + L3 一致性综合案例）
- **前端对照**：[[wiki/synthesis/react-architecture-stack.md|React 架构栈]]

## 来源

- [[wiki/sources/articles/backend-architecture-article.md|后端架构知识资料]] — 架构模式 / 微服务 / 云部署的基础综述
