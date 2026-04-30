---
project: 2026-04-aitutor-arch
status: active
created: 2026-04-29
updated: 2026-04-30
---

# 支柱 A：自研 Agent 图引擎 StateGraphLite

> 当 AI 家教需要同时调用多个 LLM、等待最快的一路给出答案、再统一决策时，该怎么做？这篇文章拆解 StateGraphLite——一个为实时语音场景量身打造的轻量图引擎，以及它在 DefaultAgentMainGraph 中的业务应用。

**代码位置**
- 引擎：`aitutor-backend-graph-framework/src/main/java/.../graph/`
- 业务图：`aitutor-backend-graph/src/main/java/.../graph/defaultagent/`

---

## 1. 为什么需要一个图引擎

先看一张真实的业务拓扑：

```
START
 ├── run_core_subgraph    ← 真正的 LLM 对话
 └── run_waitbot_subgraph ← 另一个 LLM 问"要不要让学生等一下"
          ↓ 等两者完成
     route_wait_result
      ├── shouldWait=true  → 取消上面的 LLM，发占位信号给学生
      └── shouldWait=false → 直接用 LLM 结果
```

这里有三个并发问题同时出现：

1. **两个 LLM 要并行跑**——等一个再等另一个会损失几百毫秒
2. **合流点要等两者都完成**——`route_wait_result` 只有在两个子图都出结果后才能决策
3. **失败者要被取消**——决策之后，未被选中的 LLM 请求要立刻断开，不继续花 token

用 if-else + CompletableFuture 手写这套逻辑：不是不能写，而是每加一个 LLM 调用，代码复杂度就乘以一次。图引擎的价值是**把这套并发编排变成声明式的**——你描述"谁依赖谁"，引擎负责执行顺序和合流。

---

## 2. 图的基本结构

StateGraphLite 的三个核心概念：

**节点（Node）**：一个异步计算单元。输入是"参数包"（来自入边的映射），输出是"节点结果"（供出边使用）。每个节点是独立可测的函数。

**边（Edge）**：
- **直接边**：A 完成后启动 B，可以附带参数映射（把 A 的输出写入 B 的参数包）
- **条件边**：A 完成后，根据路由键决定走向 B 还是 C

**参数包（Parameter Map）**：每个节点有一个命名参数集合，由入边写入。节点启动时能读到所有参数。这取代了传统图里的"共享状态对象"——没有全局可变 state，数据通过边显式流动。

---

## 3. 令牌驱动的合流：最优雅的设计

合流（fan-in）是图引擎最难处理的部分。`route_wait_result` 要等两个前驱都完成——传统做法是写一个显式的 `barrier` 或 `join`。

StateGraphLite 的做法是**预计算 + 令牌计数**：

**编译时**：引擎扫描所有边，计算每个节点有多少个不同的前驱节点。`route_wait_result` 的前驱是两个子图，所以它需要 2 个令牌。

**运行时**：每当一个前驱完成，它向目标节点"发送一个令牌"。令牌数达到要求时，节点自动启动。

```
run_core_subgraph 完成     → route_wait_result 收到令牌 1/2，继续等
run_waitbot_subgraph 完成  → route_wait_result 收到令牌 2/2，启动！
```

**不需要任何显式 join 声明**。只要有多条入边，就自动等所有前驱。图的拓扑结构本身成为了同步规范——你在画图的时候，合流行为就已经被隐式定义了。

---

## 4. 线程模型：单协调者 + 多工作者

多个节点并行运行，必然涉及并发安全。StateGraphLite 的选择：**一把 ReentrantLock，管所有图状态**。

规则是：每个节点的计算（真正耗时的 HTTP 请求等）在工作线程里自由并发，但完成后的回调必须回到**同一个 Executor** 抢锁，再修改共享的图状态（令牌计数、节点结果等）。

这是"单线程协调者 + 多线程工作者"的经典模式。好处是：没有死锁风险，状态竞争消失，逻辑简单。节点的业务代码可以随意并发，框架层永远是单线程协调。

---

## 5. 编译期类型校验：把问题暴露在启动时

图引擎有一个隐患：边的"参数映射"在运行时才执行，类型错误会在图跑一半时才爆炸——恰好是学生上课时。

StateGraphLite 的做法是**编译期样本值校验**：`compile()` 时，对每条边生成一个"空壳样本对象"，在上面模拟运行一遍参数映射。如果抛出 `ClassCastException`，在应用**启动时**就报错，而不是在运行时。

这个设计是 best-effort 的（依赖类型的可反射构造），但实践中能捕获绝大多数类型配置错误，大幅减少线上调试时间。

---

## 6. 子图：可组合的积木

业务图一旦复杂，单张平图的问题立刻显现：难以复用、难以测试、难以理解。

StateGraphLite 的方案是**把子图当作普通节点挂入父图**。从父图视角，`run_core_subgraph` 就是一个普通节点，只是它内部跑的是另一张完整的图。

子图和父图共享 `graphInput`（业务上下文对象）和 `Executor`（同一个线程池）。父图传入的参数包作为子图的起始参数，子图的产出被提升为节点输出——父图完全感知不到子图的内部结构。

带来的好处：每一层的子图都是**独立可测**的。`FastSlowRouterSubGraph` 在单元测试里直接 `new` 出来，传入 mock LLM，验证路由逻辑——完全不需要启动整张主图。

---

## 7. 实时流范式：图的产物是一个 Flowable

StateGraphLite 和 LangGraph 有一个根本性差异。

LangGraph 的范式是**状态收敛**：图跑完，产出一个最终状态对象。适合"给我一个答案"的场景。

StateGraphLite 的范式是**实时流**：图的产物是一个 `Flowable<LLMConversationData>`——一个可订阅的句子流。图本身跑得很快（只是在做调度和决策），真正的内容是流式产出的：

```
invokeAsync() 立刻返回一个 Flowable（此时图还没跑）
     ↓ 订阅后图开始工作
图决策: 用预测流? 用 QuickBot? 用 SlowBot?
     ↓ 决策完成，"接通"那条流
流式推送: 第1句 → 第2句 → 第3句 ... → 完成
```

这和 AI 家教的场景天然契合：学生在等待时，老师的第一句话到来比等全部回答更重要。"第一句到达的延迟"和"整个回答完成的延迟"被彻底解耦。

---

## 8. 业务图 DefaultAgentMainGraph：全景解读

有了上面的基础，再看 DefaultAgentMainGraph 就清晰多了。

### 主图：两路并行决策

```
START
 ├── run_core_subgraph    ← 主线：真正的 LLM 对话
 └── run_waitbot_subgraph ← 旁支：需不需要先给学生一个等待信号？
          ↓ fan-in 等两路完成
     route_wait_result
      ├── shouldWait=true  → build_wait_mock（取消 core，发占位 Flowable）
      └── shouldWait=false → 直接用 core 的 Flowable
```

大多数情况下 WaitBot 返回 false，主线直通。但有了这一路判断，AI 家教可以在"正在努力思考"时先播放一段占位音频，而不是让学生面对静默。

### DoCommitCoreSubgraph：预测优先

```
predicted_match
 ├── 命中 → 直接用上一轮预热好的 LLM 流（延迟 ≈ 0）
 └── 未命中 → GetLlmFlowableSubgraph（发起新 LLM 请求）
```

上一轮老师说完最后一句时，系统已经预测"学生下一句可能说什么"，提前发起了 LLM 请求并开始缓存（`replay().connect()`）。如果预测命中，学生说完话时 LLM 数据已经在路上了，延迟趋近于 0。

### FastSlowRouterSubGraph：4 路并行竞速

这是整个架构里最精妙的设计之一：

```
4 路同时出发：
  CLOSED_PROBLEM_ROUTER   ← 判断：是封闭性问题吗？
  STUDENT_ANSWER_ROUTER   ← 判断：是学生回答场景吗？
  QUICK_BOT               ← 正式开始生成"快思考"回答
  SLOW_BOT                ← 正式开始生成"慢思考"回答
         ↓ fan-in 等 4 路完成
  route_selector 裁决：
    Router 有命中 → 选 QuickBot，取消 SlowBot
    Router 无命中 → 选 SlowBot，取消 QuickBot
```

关键点：**QuickBot 和 SlowBot 不等 router 决策，直接开始跑**。当 router 出结果时，QuickBot/SlowBot 的数据已经流了一部分。被选中的那路继续，未选中的 HTTP 连接立刻断开（停止花 token）。

这是典型的"预测性执行"——提前花一点资源，换取更低的关键路径延迟。router 决策本身很快（毫秒级），而 LLM 生成很慢（秒级），所以并发启动的收益巨大。

还有一个细节：`replay().connect()` 的作用。每一路的 `Flowable` 在子图节点里就做了 `connect()`——无论下游有没有人订阅，上游 HTTP 连接就开始建立、数据就开始流进缓冲。等到真正被选中时，那路的数据可能已经到了几句，订阅者直接回放缓冲内容，再接上实时流。

---

## 9. 取消语义：三层联动

整套取消链路：

```
外部 dispose（学生打断）
  → Flowable.doOnCancel() → runFuture.cancel(true)
    → 节点的 CoreNodeOutput.cancel()
      → DisposableCancelable.dispose()
        → ConnectableFlowable.connection.dispose()
          → HttpURLConnection.disconnect()   ← 真正停止花 token
```

三层各有必要：
- **外层**：停止向下游推送新元素
- **中层**：节点内部的 LLM 请求停止消费
- **内层**：HTTP 连接释放，token 计费停止

业务上有三个取消时机：WaitBot 抢占 core、竞速放弃未选中路、学生打断整轮对话——三种场景都走这条三层链路。

---

## 10. 小结

StateGraphLite 的核心设计哲学：**让图的拓扑结构本身成为并发规范**。

- 有多条入边 → 自动 fan-in，不需要显式 join
- 有子图 → 等价于节点，统一抽象
- 有取消需求 → 从 Flowable 层一路传导到 HTTP 层
- 有流式输出 → 图的产物是 Flowable，而不是状态包

这些设计放在一起，使得业务开发者可以"画图"来表达并发逻辑，而不是手写并发代码。

---

## 附：代码地图

| 主题       | 文件                                                                                                                |
| -------- | ----------------------------------------------------------------------------------------------------------------- |
| 图构建 DSL  | `StateGraphLite.java`                                                                                             |
| 图执行引擎    | `CompiledStateGraphLite.java`（重点看 `ExecutionSession`）                                                             |
| 节点 / 边契约 | `GraphNode.java`, `GraphNodeResult.java`, `GraphEdgeParamMapper.java`                                             |
| 主图       | `DefaultAgentMainGraph.java`                                                                                      |
| 子图       | `DoCommitCoreSubgraph.java`, `WaitbotSubgraph.java`, `GetLlmFlowableSubgraph.java`, `FastSlowRouterSubGraph.java` |
| 上下文      | `DefaultAgentGraphContext.java`                                                                                   |
