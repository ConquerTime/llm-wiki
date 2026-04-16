---
title: AI Agent
type: concept
subtype: ai
tags: [ai-agent, llm, autonomous, planning, memory, tool-use]
created: 2026-04-15
updated: 2026-04-15
sources:
  - ../../raw/articles/OpenClaw + AI Agent 面试八股文：背完这篇，你懂的比面试官还多！.md
---

# AI Agent

> 具备自主规划、记忆和工具调用能力、能自主完成多步骤目标导向任务的 AI 系统，核心从"回答问题"升级为"完成目标"。

## 标准公式

**Agent = LLM（大脑）+ Planning（规划）+ Memory（记忆）+ Tool Use（工具）**

与传统 Chatbot 的区别：Chatbot 只做对话（单轮/多轮），Agent 有自主规划、长短期记忆和工具调用能力，能独立完成多步骤任务。

## 四大基础组件

### 1. LLM（大脑）
负责理解意图、生成文本、进行逻辑判断。是 Agent 的决策核心。

### 2. Planning（规划）
将复杂目标拆解为可执行子任务。主要方法：
- **CoT**（Chain of Thought）：逐步线性推理，适合逻辑清晰的简单任务
- **ToT**（Tree of Thought）：树状搜索多条推理路径，适合多种可能解的复杂问题
- **Reflexion**：自我反思优化，适合需要迭代改进的任务
- **Plan-and-Solve**：先生成整体计划再逐步执行，适合步骤可预见的多步任务
- **[[react-framework|ReAct]]**：推理+行动交替，适合不确定性高、需要与外部环境交互的任务

### 3. Memory（记忆）
- **短期记忆**：上下文窗口中的对话历史和当前任务状态，随会话结束消失
- **长期记忆**：持久化存储（向量数据库、Markdown 文件等），跨会话保留

实现方案对比：

| 方案 | 特点 | 适用场景 |
|------|------|----------|
| 上下文窗口 | 简单，受窗口限制 | 短会话 |
| 向量数据库 | 语义检索，容量大 | 大量非结构化知识 |
| Markdown 文件 | 人类可读可编辑（[[openclaw|OpenClaw]] 方案）| 本地优先场景 |
| 混合方案 | 向量 + 关键词 + 图数据库 | 生产级系统 |

### 4. Tool Use（工具调用）
详见 [[function-calling|Function Calling]]。

## 核心风险：幻觉-行动放大

Agent 的幻觉不只是"说错话"，而会通过工具调用**实际执行**错误操作（发送错误邮件、删除文件）。自主性越强，爆炸半径越大。

## 自主性的五个维度

1. 无需逐步指导，独立运作
2. 感知环境变化并调整（反应性）
3. 有目标导向的主动行为（主动性）
4. 与人类自然交互（社交能力）
5. 从历史中学习改进（学习能力）

## Human-in-the-loop 设计模式

1. **审批门控**：关键操作前暂停等待人类确认
2. **主动询问**：信息不足时主动向用户提问
3. **异常升级**：遇到无法处理的错误时通知人类
4. **定期检查点**：长任务中定期汇报进度

## 评估指标

任务完成率 / 步骤效率（ReAct 循环次数）/ token 消耗 / 幻觉率 / 鲁棒性 / 延迟

## 开放问题

- 如何在自主性和安全性之间取得平衡？
- 多步骤任务中错误传播如何有效缓解？
- Agent 评估基准尚不成熟，如何可靠度量"真实任务完成率"？

## 来源

- [[sources/articles/openclaw-ai-agent-interview|OpenClaw + AI Agent 面试八股文]]

## 相关项目

- [[openclaw|OpenClaw]] 系列 Agent Brain（如 [[gbrain]]）展示了本地优先的 Brain 架构
- [[nuwa-skill]] 的六路 Agent 并行调研 + 双 Agent 精炼是 Multi-Agent 协作的实战案例
