---
project: 2026-04-aitutor-arch
status: active
created: 2026-04-29
updated: 2026-04-29
---

# AI 家教技术架构萃取 · 简报

## 背景

`aitutor-backend` 是一个 AI 驱动的实时语音教学系统（家教机器人），核心是一个 Java/RxJava 多模块 Maven 项目。
系统需要在低延迟下完成：ASR 识别 → Agent 路由 → 流式 LLM 推理 → TTS 合成 → WebSocket 下发，同时支持打断、预测输入、多 Bot 竞速等复杂交互。

触发本项目：需要系统性地把 aitutor-backend 的架构知识沉淀到 wiki，供后续技术决策和知识回流使用。

## 目标

产出一份可供他人快速理解的技术架构文档，覆盖：
1. Agent 图设计（StateGraphLite 框架 + DefaultAgentMainGraph 图拓扑）
2. 实时 AI 语音对话链路（ASR→LLM→TTS 时序 + 打断机制）
3. LLM 提供商抽象层（多 provider 支持，含语音原生 AudioChatLlama）
4. 状态管理与评估策略（StateStore 版本迁移 + 集成测试框架）

## 非目标

- 不覆盖前端 / 客户端代码
- 不深入分析具体 prompt 设计
- 不覆盖 CI/CD、基础设施配置

## 范围

- 仓库：`/Users/zhouyangdong/Documents/projects/horizon/aitutor-backend`
- 核心模块：`aitutor-backend-graph`、`aitutor-backend-llm`、`aitutor-classroom-legacy`（RTC 运行时）、`aitutor-classroom-java`（StateStore）
- 参考文档：`docs/LLM响应处理流程文档.md`、`docs/StateStore迁移集成测试框架—开发者手册.md`

## 已知架构要点（启动时扫描所得）

### 1. Agent 图框架：StateGraphLite

自研轻量 Agent 图引擎（类 LangGraph），核心组件：
- `StateGraphLite<C>` — 图构建 DSL：addNode / addEdge / addConditionalEdges
- `CompiledStateGraphLite<C>` — 编译后的图，`run(context, executor)` 返回 `TracingCompletableFuture<GraphRunResult>`
- 节点（`GraphNodeContext` → `GraphNodeResult`）、边（`GraphEdgeParamMapper` 做参数传递）
- `GraphRunResult` 含 `nodeExecutionDetailMap`（startOffsetMs / endOffsetMs / costMs），支持 timeline 打点

### 2. DefaultAgentMainGraph 拓扑

```
START
  ├── run_core_subgraph (DoCommitCoreSubgraph)
  └── run_waitbot_subgraph (WaitbotSubgraph)
         ↓ 等两路都完成
  route_wait_result
    ├── [shouldWait=true]  → build_wait_mock → END (返回 LLMMockWait Flowable)
    └── [shouldWait=false] → END (直接返回 coreOutput.flowable)
```

- 两路**并行**启动（START 同时触发 core + waitbot）
- `route_wait_result` 是 fan-in 节点：等两路完成后决策
- 如果 waitbot 判断"应该等待"，立即 cancel core 请求，返回等待占位信号

### 3. DoCommitCoreSubgraph（LLM 请求核心子图）

```
START → predicted_match
  ├── [hit]  → END（直接复用预热流，避免重复 LLM 调用）
  └── [miss] → run_get_llm_subgraph (GetLlmFlowableSubgraph → FastSlowRouterSubGraph)
```

- **预测优化**：`UserInputPredictedTask` 在上一轮最后一句时提前 replay+connect 热身 Flowable，命中则 0 延迟复用
- **FastSlowRouterSubGraph**：
  - 首轮 → 直接 slowBot
  - 非首轮 → 4 路**并行**（closedProblemRouter / studentAnswerRouter / quickBot / slowBot）
  - fan-in 后：closedHit || studentHit → 取 quickBot，否则取 slowBot；另一路 cancel
  - quickBot = 封闭问题/简短回答模型；slowBot = 完整教学响应模型

### 4. 实时语音对话链路（ASR→LLM→TTS）

```
客户端 ASR音频流
  → AsrComplete 事件
  → StudentActivityManager.checkActivity()
  → RoundStart.submitLLM()
      ├── 构建 LLMConversationContext（历史 + 当前输入 + Section 配置）
      └── llmConversationService.chatWithLLm() [RxJava subscribeOn LLMExecutor]
            ↓ 流式逐句返回 LLMConversationData
  LlmResponseHandlerImpl.onEvent(sentence)
      ├── 检测 <end> 标签（sectionOver）
      ├── asyncGenerateTts(talkSentence)   ← 并行
      ├── asyncGeneratePostPptBoardCommands ← 并行
      └── thenCombine → buildTeacherMessage → eventBus.publish(TeacherMessageEvent)
            ↓
  RoundStart.handlerThisRoundEvent()
      ├── processNavigateCommands
      ├── onGenImage（异步）
      ├── buildAudioMessage → StandardAudioMessageBundle
      │     ├── StandardAudioMessage（音频+textAudioIntervalsList 字幕时间轴）
      │     ├── StandardBoardCommandMessage（板书）
      │     ├── StandardEmotionMessage（表情）
      │     └── StandardClassBreakMessage（课间休息）
      └── [未被打断] sendAudioMessage(bundle) → WebSocket → 客户端
```

**打断机制**：AsrBreak/AsrStartBreak → setTeacherInterrupted(true) + dispose LLM 订阅，后续 event 检查标志跳过发送。

**最后一句逻辑**：isLastRoundAudio=true 时触发 `predictedUserInput()`（预测下轮输入）+ 可能触发 SectionOverLLMEvent。

### 5. LLM 提供商抽象层

接口：`LLM.aCommit(List<LLMMessage>, LLMRuntimeConfig) → Flowable<LlmStreamResult>`

已实现的 Provider：
| Provider | 说明 |
|----------|------|
| OpenaiLLM | 标准 OpenAI SSE 流式 |
| GeminiLLM | Google Gemini |
| DeepseekLLM | DeepSeek |
| TongyiLLM | 阿里通义 |
| VLLM | 自托管 vLLM 推理服务 |
| KanyunLLM | 内部模型服务 |
| AnthropicClaudeLLM | Anthropic Claude |
| **AudioChatLlamaLLM** | 语音原生 LLM：直接接收 PCM/URL 音频，`audio_hex` 或 `audio_url` 格式，支持 `system_id` 短系统提示 |

`LLMRegistry` + `LLMDynamicConfig` 管理多 provider 路由；`LLMRuntimeConfig` 包含 temperature / topP / shortSystemMode 等运行时参数。

### 6. 状态管理与评估（StateStore）

- **StateStore** 是教室运行时状态的统一存储，支持版本化迁移（`StateStoreVersionDefinition`）
- **版本链**：v1 → v2(ModuleState) → v3(PptState) → v4(AgentState) → v5(TeachingToolState) → v6...
- **迁移机制**：
  - `copyFrom` 自动复制同名同类型字段
  - `migrate()` 只处理：新增字段设默认值 / 从旧字段回填 / 类型变更
- **集成测试**：`StateStoreMigrationTestModules` 为单一版本清单入口；从线上 OSS 下载真实快照，按 module version 裁剪 engine 做迁移 + `ResourceSnapshotSemanticSpec` 语义断言

## 交付物

- [ ] `deliverables/arch-overview.md` — 整体架构全景图（含 Agent 图拓扑、语音链路时序）
- [ ] `deliverables/agent-graph-design.md` — Agent 图框架深度分析（StateGraphLite vs LangGraph 对比）
- [ ] `deliverables/voice-pipeline.md` — 实时语音对话链路详解（延迟分析 + 打断/预测设计）
- [ ] `deliverables/llm-providers.md` — LLM 多 Provider 架构及 AudioChatLlama 语音原生方案
- [ ] `deliverables/evaluation-strategy.md` — StateStore 迁移测试框架 + 评估策略

## 里程碑

- [ ] 架构全景 + Agent 图分析 — 预计 2026-05-03
- [ ] 语音链路 + LLM 层分析 — 预计 2026-05-07
- [ ] 评估策略文档 + 知识回流到 wiki — 预计 2026-05-10

## 风险 / 未知

- `aitutor-backend-graph-framework` 模块（StateGraphLite 的底层实现）尚未深读，图引擎内部并发模型待确认
- `WaitbotSubgraph` 内部逻辑未读（shouldWait 判断依据未明）
- TTS 供应商和延迟数据未知
- 性能指标（ASR→首句 TTS 延迟、整体 p99）未从代码中找到，可能在监控系统而非代码
