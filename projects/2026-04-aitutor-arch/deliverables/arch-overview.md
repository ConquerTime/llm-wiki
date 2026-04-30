---
project: 2026-04-aitutor-arch
status: active
created: 2026-04-29
updated: 2026-04-29
---

# aitutor-backend 架构全景

> AI 家教实时语音教学系统的一页架构地图。三大支柱：**Agent 图框架（StateGraphLite）**、**实时语音对话链路（ASR→LLM→TTS）**、**状态管理与评估（StateStore + 迁移测试）**。

---

## 1. 模块拓扑

```
aitutor-backend
├── aitutor-backend-graph-framework   # 通用图引擎：StateGraphLite / CompiledStateGraphLite
├── aitutor-backend-graph             # 业务图定义：DefaultAgentMainGraph + 子图们
├── aitutor-backend-llm               # LLM 抽象层：LLM / LLMRegistry / 8 个 Provider
├── aitutor-classroom-legacy          # 教室运行时（RTC、RoundStart、LlmResponseHandlerImpl）
├── aitutor-classroom-java            # StateStore 版本化存储 + 迁移引擎
├── aitutor-classroom-java-admin      # 运维工具（含 SnapshotDevToolController）
├── aitutor-classroom-live-widget     # 实时组件
└── aitutor-classroom-java-client/backend/job/common  # 支撑性模块
```

**依赖方向**：`classroom-legacy`（运行时） → `backend-graph`（Agent 编排） → `backend-graph-framework`（图引擎）＋`backend-llm`（LLM 抽象）。

---

## 2. 三大支柱

### 支柱 A：Agent 图框架（StateGraphLite）

自研轻量版 LangGraph，位于 `aitutor-backend-graph-framework`。

**核心抽象**

| 组件 | 职责 |
|------|------|
| `StateGraphLite<I>` | 图构建 DSL：`addNode` / `addEdge` / `addConditionalEdges` / `setEndParameterTypes` |
| `CompiledStateGraphLite<I>` | 编译后图，`run(input, executor, startParams) → TracingCompletableFuture<GraphRunResult>` |
| `GraphNode<I>` | 节点函数：`GraphNodeContext → TracingCompletableFuture<GraphNodeResult>` |
| `GraphEdgeParamMapper` | 边映射：把 fromNode 的 output 写入 toNode 的 parameterMap |
| `GraphNodeResult.routeKey` | 条件边的路由键，决定走哪条 route |
| `GraphRunResult` | 运行结果：`endNodeParameterMap` + `nodeExecutionDetailMap`（startOffsetMs/endOffsetMs/costMs） |

**并发模型**（见 `CompiledStateGraphLite.ExecutionSession`）

1. **Token 驱动 fan-in**：每个节点预计算 `requiredIncomingTokenCount`（前驱节点数），前驱完成时推送 token 到目标节点，到达数 ≥ 需求数才启动，实现自然的 fan-in 合流
2. **ReentrantLock 会话锁**：`sessionLock` 保护 `startedNodeSet` / `arrivedTokenCount` / `completedNodeResultMap`，节点完成回调统一回到同一 `executor` 再抢锁
3. **子图挂载**：`addNode("name", subgraph.compiled(), ...)` 子图以一个节点的形式嵌入主图，执行明细以 `parent-childNode` 前缀合并到顶层 timeline
4. **参数类型校验**：`nodeParameterTypeMap` 声明节点期望的参数类型，边写入时做类型检查，启动前强制必填校验
5. **取消传播**：`TracingCompletableFuture.cancel(true)` → 主图的 `doOnCancel` → 触发订阅侧清理

### 支柱 B：实时语音对话链路

端到端时序（见 `docs/LLM响应处理流程文档.md`）：

```
客户端 ASR音频流
  → AsrComplete
  → StudentActivityManager.checkActivity()
  → RoundStart.submitLLM()
       └── 构建 LLMConversationContext（历史 + 当前输入 + Section 配置）
            └── llmConversationService.chatWithLLm()  [subscribeOn LLMExecutor]
                 └── DefaultAgentMainGraph.invokeAsync() ← 图执行
                      ↓ 流式逐句 LLMConversationData
  LlmResponseHandlerImpl.onEvent(sentence)
       ├── 检测 <end> 标签 → sectionOver
       ├── asyncGenerateTts(talkSentence)           ← 并行
       ├── asyncGeneratePostPptBoardCommands        ← 并行
       └── thenCombine → buildTeacherMessage
            ├── 解析指令：生图/表情/板书/翻页/奖励/课间休息
            └── eventBus.publish(TeacherMessageEvent)
  RoundStart.handlerThisRoundEvent()
       ├── [未被打断] buildAudioMessage → StandardAudioMessageBundle
       │     ├── StandardAudioMessage（音频 + textAudioIntervals 字幕时间轴）
       │     ├── StandardBoardCommandMessage（板书）
       │     ├── StandardEmotionMessage（表情）
       │     └── StandardClassBreakMessage（课间）
       ├── sendAudioMessage(bundle) → WebSocket → 客户端
       └── [isLastRoundAudio] predictedUserInput()（预热下一轮 LLM）
```

**关键设计**

- **流式逐句**：LLM 以句子为单位返回，每句独立走 TTS / 板书生成，**不等全句完成**
- **打断机制**：`AsrBreak/AsrStartBreak` → `teacherInterrupted=true` + `llmDisposable.dispose()` → 后续 event 检查标志跳过发送
- **字幕同步**：`textAudioIntervalsList` 携带文字-音频时间轴，客户端按时间轴渲染字幕
- **Last-frame 协议**：`isLastRoundAudio` 标记本轮最后一句，客户端据此切换状态
- **SectionOver 事件**：LLM 输出 `<end>` 标签表示小节结束，最后一句后发 `SectionOverLLMEvent` 驱动课程推进

### 支柱 C：状态管理与评估（StateStore）

- **StateStore** 是教室运行时状态的统一版本化存储
- **版本链**：v1 → v2(ModuleState) → v3(PptState) → v4(AgentState) → v5(TeachingToolState) → v6...
- **迁移机制**：`copyFrom` 自动复制同名同类型字段 → `migrate()` 只处理新增字段默认值 / 旧字段回填 / 类型变更
- **评估测试**（见 `docs/StateStore迁移集成测试框架—开发者手册.md`）：
  - `StateStoreMigrationTestModules.currentModules()` 是唯一的版本清单入口
  - 从线上 OSS 拉取真实快照（Snapshot JSON + InRoomClass JSON）
  - 按 module version 裁剪 engine，做迁移 + `ResourceSnapshotSemanticSpec.assertMigrated()` 字段级语义断言
  - Admin 工具 `SnapshotDevToolController` 一键下载线上快照并上传到 internal OSS

---

## 3. DefaultAgentMainGraph 完整图拓扑

```
                    ┌────────────────────────────────────┐
                    │             START                   │
                    └────────┬──────────────┬─────────────┘
                             │              │
                             ▼              ▼
                 ┌──────────────────┐  ┌──────────────────┐
                 │ run_core_subgraph │  │run_waitbot_subgraph│
                 │ (DoCommitCore)    │  │  (Waitbot)        │
                 └────────┬─────────┘  └─────────┬─────────┘
                          │                       │
                          └───────────┬───────────┘
                                      ▼
                          ┌─────────────────────────┐
                          │   route_wait_result     │ ← fan-in
                          └──────┬───────────┬──────┘
                shouldWait=true  │           │  shouldWait=false
                                 ▼           ▼
                  ┌──────────────────────┐   END (返回 core.flowable)
                  │   build_wait_mock    │
                  │ (取消 core，发占位)   │
                  └──────────┬───────────┘
                             ▼
                            END (返回 LLMMockWait Flowable)
```

### 3.1 DoCommitCoreSubgraph：预测命中 → 跳过 LLM

```
START → predicted_match ─[hit]─→  END (复用预热流，0 延迟)
                       └[miss]─→  GetLlmFlowableSubgraph
```

### 3.2 GetLlmFlowableSubgraph：路由策略分叉

```
START ─[useFastSlowBot]─→  FastSlowRouterSubGraph
       └[simple]────────→  simple_lecturing (LECTURING_BOT 单一请求)
```

### 3.3 FastSlowRouterSubGraph：4 路竞速

```
                        START
                          │
            ┌─[firstRound]─┴─[nonFirstRound]─┐
            ▼                                 ▼
  first_round_slow_bot_request       non_first_round_fanin
            │                     (一扇出 4 路并行启动)
            │                      ├── closed_problem_router
            │                      ├── student_answer_router
            │                      ├── quick_bot_request (QUICK_BOT)
            │                      └── slow_bot_request  (SLOW_BOT)
            │                                 │
            │                                 ▼
            │                          route_selector (fan-in 4)
            │                  ┌────────────────┴──────────────────┐
            │         closedHit||studentHit=true        两 router 都 false
            │                  ▼                                   ▼
            │              选 quick 丢 slow                  选 slow 丢 quick
            │                  │                                   │
            ▼                  └─────────────────┬─────────────────┘
           END (coreOutput)                      ▼
                                                END (coreOutput)
```

**AssistantType 枚举**（`aitutor-backend-llm/llm/constants/AssistantType`）：
- `LECTURING_BOT`（主授课）
- `WAIT_BOT`（是否等待判断）
- `QUICK_BOT` / `SLOW_BOT`（快/慢思考，均为 Gemini）
- `CLOSED_PROBLEM_ROUTER` / `STUDENT_ANSWER_ROUTER`（路由判断）
- `PREDICTED_BOT`（用户输入预测）
- `COMPRESSION_BOT`（上下文压缩）
- `RECOMMENDATION_BOT`（推荐）

---

## 4. 延迟优化清单

| 优化 | 机制 | 收益 |
|------|------|------|
| **预测命中复用** | 上一轮最后一句触发 `UserInputPredictedTask` → replay+connect 预热 `PREDICTED_BOT`；`predicted_match` 节点命中直接返回热流 | 命中时下一轮 LLM 延迟降为 ~0 |
| **并行生成** | core 子图 ‖ waitbot 子图，LLM 逐句 ‖ TTS ‖ 板书生成 | 首句 TTS 到达时间 ≈ max(LLM首句, TTS单句) 而非串行累加 |
| **快慢竞速** | 非首轮 4 路并行（2 router + quick + slow），router 决策未选中路径立即 cancel | 快问题 ~QUICK_BOT 延迟；慢问题不比单独 slow 慢 |
| **Replay 预连接** | `sourceFlowable.replay().connect()` 在子图节点里就开始发 HTTP 请求，等到真正订阅时数据已在缓冲 | 节点间传递 Flowable 不丢失已到达的 token |
| **取消传播到 HTTP** | `emitter.setCancellable` → `HttpURLConnection.disconnect()`，上游主动 cancel 时断开连接节省 token | 竞速未选中路径、waitbot 抢占、用户打断均能立即停止花费 |
| **连接超时 4s / 读超时 20s** | `AudioChatLlamaLLM` 中显式设置 | 故障快速失败，避免长期占用 |

---

## 5. LLM 抽象层速览

**接口**：`LLM.aCommit(List<LLMMessage>, LLMRuntimeConfig) → Flowable<LlmStreamResult>`

**Provider 列表**：

| Provider | 特点 |
|----------|------|
| OpenaiLLM / GeminiLLM / AnthropicClaudeLLM | 标准 SSE 流式 |
| DeepseekLLM / TongyiLLM / KanyunLLM | 国内模型 |
| VLLM | 自托管 vLLM 推理服务 |
| **AudioChatLlamaLLM** | 语音原生 LLM：直接接收 PCM hex 或 URL 音频（`audio_hex` / `audio_url`），使用 `<\|audio\|>` 占位符，支持 `system_id` 短系统提示压缩 |

**配置**：`LLMRegistry`（provider 路由）+ `LLMDynamicConfig`（热配置）+ `LLMRuntimeConfig`（单次调用的 temperature/topP/shortSystemMode）。

---

## 6. 可延展文档（deliverables 路线）

- `agent-graph-design.md` — StateGraphLite 深度分析（token 模型 / 子图挂载 / 与 LangGraph 对比）
- `voice-pipeline.md` — 语音链路详解（端到端延迟拆解 / 打断设计 / 预测 task）
- `llm-providers.md` — 多 Provider 设计与 AudioChatLlama 语音原生方案
- `evaluation-strategy.md` — StateStore 迁移测试框架（语义断言模式 / 版本裁剪）

---

## 7. 已知空白

- TTS 供应商与延迟数字 — 待在 `TeacherMessageService` 中确认
- 监控指标（ASR→首句 TTS p50/p99）— 可能在外部监控系统而非代码
- `COMPRESSION_BOT` / `RECOMMENDATION_BOT` 在图中的挂载位置 — 未见于 `DefaultAgentMainGraph`，可能由其他上层组件调度
