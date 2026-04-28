---
title: ReAct 框架
type: concept
subtype: ai
tags: [ai, ai-agent, llm]
created: 2026-04-15
updated: 2026-04-15
sources:
  - ../../raw/articles/OpenClaw + AI Agent 面试八股文：背完这篇，你懂的比面试官还多！.md
---

# ReAct 框架

> **ReAct = Reasoning + Acting**，让 LLM 在推理和行动之间交替循环，通过观察行动结果不断调整策略——目前最主流的 Agent 执行模式。

## 核心循环

```
Thought（推理）→ Action（行动）→ Observation（观察）→ 重复，直到任务完成
```

- **Thought**：LLM 分析当前状态，推理决定下一步
- **Action**：根据推理结果执行具体操作（调用工具、查询 API 等）
- **Observation**：收集执行结果，作为下一轮推理的输入

循环终止条件：找到最终答案 / 达到最大迭代次数 / 遇到无法继续的错误

## 与 CoT 的对比

| 维度 | CoT（链式思维）| ReAct |
|------|--------------|-------|
| 核心能力 | 纯推理，逐步分解问题 | 推理 + 行动，与外部环境交互 |
| 信息来源 | 仅依赖模型内部知识 | 可调用外部工具获取实时数据 |
| 幻觉风险 | 高（无法验证事实）| 低（通过工具调用获取真实数据）|
| 适用场景 | 数学推理、逻辑分析 | 需要执行操作的复杂任务 |

> "CoT 是让模型'想清楚'，ReAct 是让模型'想清楚然后动手干'。"

## 关联框架

- **CoT**：ReAct 的 Thought 步骤可以内嵌 CoT
- **ToT**：树状搜索多条推理路径，可与 ReAct 结合
- **Reflexion**：ReAct 循环失败后触发自我反思，是 ReAct 的补充
- **Plan-and-Solve**：先生成完整计划再执行，适合可预见任务；ReAct 边想边做，适合高不确定性任务

## 在 OpenClaw 中的实现

[[openclaw|OpenClaw]] 的 Brain 组件实现 ReAct：
1. 组装系统提示词（含可用工具列表）
2. 发送给 LLM
3. LLM 输出推理和工具调用请求
4. Brain 解析并执行工具调用
5. 将结果返回 LLM
6. 循环直到 LLM 输出最终回复

**相关机制**：
- **Compaction**：ReAct 循环消耗大量 token 时自动压缩上下文
- **Steering while streaming**：用户在流式推理时发送新消息，Agent 在下一个 tool call 后注入
- **序列化**：通过 per-session + global queue 防止竞争条件

## Token 优化

Action + Observation 通常比 Thought 更消耗 token（工具调用结果可能很大）。

优化方法：限制工具返回长度 / 设置最大迭代次数 / Compaction 压缩 / 对大结果做摘要

## 错误处理

好的 Agent 设计：
1. 将错误作为 Observation 反馈给 LLM
2. LLM 在下一个 Thought 中分析失败原因
3. 尝试替代方案或调整参数重试
4. 多次失败后升级为向用户请求帮助

## 开放问题

- 多步推理中的"错误传播"问题：某步出错后续会基于错误 Observation 继续推理，错误放大
- 最大迭代次数的合理设置（过小任务未完成，过大成本高）

## 来源

- [[sources/articles/openclaw-ai-agent-interview|OpenClaw + AI Agent 面试八股文]]
