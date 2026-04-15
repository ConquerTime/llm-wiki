---
title: Function Calling（工具调用）
type: concept
subtype: ai
tags: [function-calling, tool-use, llm, agent, json, structured-output]
created: 2026-04-15
updated: 2026-04-15
sources:
  - ../../raw/articles/OpenClaw + AI Agent 面试八股文：背完这篇，你懂的比面试官还多！.md
---

# Function Calling（工具调用）

> LLM 与外部系统交互的桥梁，让模型不只输出文本，还能返回结构化的调用指令，由运行时环境执行后将结果反馈给模型形成闭环。

## 四步流程

**Step 1：工具注册**
定义可用工具的名称、描述、参数 schema：
```json
{
  "name": "send_email",
  "description": "发送电子邮件",
  "parameters": {
    "recipient": {"type": "string"},
    "subject": {"type": "string"},
    "body": {"type": "string"}
  }
}
```

**Step 2：LLM 判断**
根据用户请求和工具描述，模型决定是否需要调用工具。

**Step 3：结构化输出**
LLM 输出 JSON 格式的调用指令：
```json
{
  "tool": "send_email",
  "args": {
    "recipient": "bob@example.com",
    "subject": "周报",
    "body": "本周完成了..."
  }
}
```

**Step 4：执行与反馈**
LLM 自身**不执行**函数，由运行时环境解析 JSON 并执行，结果返回给 LLM 作为后续推理的输入。

> 关键理解：**LLM 是"指挥官"，不是"执行者"。**

## 与 RAG 的关系

RAG 本质上是一种特殊的 Tool Calling——"检索"就是一个工具。Agent 可以通过 Tool Calling 触发 RAG 检索，获取相关文档，再基于结果生成回答。

## 与 Structured Output 的关系

Structured Output 是让 LLM 按指定 JSON Schema 输出结构化数据的能力。Function Calling 是 Structured Output 的一种特殊应用——输出的结构化数据恰好是工具调用指令。

## Parallel Tool Calling

LLM 在单次回复中返回多个工具调用请求，运行时并行执行。适合多个**相互独立**的调用（如同时查天气和查日历），不适合有依赖关系的调用。

## 常见风险

**幻觉调用**：LLM 可能调用不存在的工具、传递错误参数类型、或在不该调用时调用。

防范措施：
- 严格的 schema 验证
- 运行时检查工具名是否在注册列表中
- 参数类型强校验
- 调用频率限制

## Tool Description 设计要点

描述质量直接影响 LLM 选对工具的概率：
1. 明确说清工具做什么和不做什么
2. 参数描述包含类型、格式、示例
3. 说明边界条件和错误场景
4. 避免模棱两可的词语

## 错误处理最佳实践

1. 分类错误：区分可重试（网络超时）和不可重试（参数错误）
2. 错误信息反馈：将错误详情作为 Observation 返回给 LLM
3. 重试策略：指数退避
4. 降级方案：主工具失败时尝试替代工具
5. 超时控制：设置每个工具的执行超时

## 在 OpenClaw 中的实现

[[openclaw|OpenClaw]] 的 Core tools 包括 `read`、`exec`、`edit`、`write` 等系统工具，始终可用但受 tool policy 约束。

相关 Hook：
- `before_tool_call`：执行前拦截修改参数（认证、日志、校验）
- `after_tool_call`：结果返回前拦截修改（数据转换、脱敏、指标收集）
- `tool_result_persist`：写入 session transcript 前变换（脱敏、压缩、结构化）

## 来源

- [[sources/articles/openclaw-ai-agent-interview|OpenClaw + AI Agent 面试八股文]]
