# 核心哲学：Agent = 模型 + Harness

> 基于 shareAI-lab/learn-claude-code 整理。
> 这是所有后续学习的思想锚点，先搞清楚"我们到底在建什么"。

---

## 一句话定义

**Agent = 训练好的模型 + 让它在特定环境工作的基础设施（harness）**

- Agency（感知、推理、行动的能力）来自**模型训练**，不是外部代码
- 但一个能干活的 agent 产品需要模型和 harness **缺一不可**
- 模型是驾驶者，harness 是载具
- **我们在做的是 harness**，不是智能本身

## 反面——agent 不是什么

不是拖拽式工作流构建器、不是 if-else 节点图、不是 prompt chain。那些是"鲁布·戈德堡机械"（过度工程化的脆弱流水线），是被 LLM 贴皮的 GOFAI（经典符号 AI），早被学界抛弃的死路。

> "你不可能通过工程手段编码出 agency。Agency 是学出来的，不是编出来的。"

## Harness 的五类组成

```
Harness = Tools + Knowledge + Observation + Action Interfaces + Permissions

Tools:          文件读写、Shell、网络、数据库、浏览器
Knowledge:      产品文档、领域资料、API 规范、风格指南
Observation:    git diff、错误日志、浏览器状态、传感器数据
Action:         CLI 命令、API 调用、UI 交互
Permissions:    沙箱隔离、审批流程、信任边界
```

## Claude Code 剥到本质

```
Claude Code = 一个 agent loop
            + 工具 (bash, read, write, edit, glob, grep, browser...)
            + 按需 skill 加载
            + 上下文压缩
            + 子 agent 派生
            + 带依赖图的任务系统
            + 异步邮箱的团队协调
            + worktree 隔离的并行执行
            + 权限治理
```

就这些。**Claude Code 作为教学标本的意义：它展示了当你信任模型、把工程精力集中在 harness 上时会发生什么。**

## 最小 agent loop——30 行 Python（s01）

```python
def agent_loop(query):
    messages = [{"role": "user", "content": query}]
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=messages,
            tools=TOOLS, max_tokens=8000,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return

        results = []
        for block in response.content:
            if block.type == "tool_use":
                output = run_bash(block.input["command"])
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })
        messages.append({"role": "user", "content": results})
```

**这就是整个 Agent**。后面 11 个章节都在这个循环上叠加机制 —— **循环本身始终不变**。

## 本项目的定位

我们的学习项目正是在这个哲学下展开：

- **不学**怎么训练模型（那是 Anthropic/DeepMind 的事）
- **学**怎么建 harness：工具系统、上下文管理、权限、多 agent 协作
- **动手做**：按 s01 → s12 递进，每一步只加一个 harness 机制
- **对照源码**：每学一个机制，去看 Claude Code 真实源码怎么实现的（cc-haha 版本）
