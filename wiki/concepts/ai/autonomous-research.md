---
title: 自主 ML 研究（Autonomous ML Research）
type: concept
subtype: ai
tags: [ai-agent, ml-research, autonomous, experiment]
created: 2026-04-16
updated: 2026-04-16
sources:
  - ../../../raw/articles/karpathy-autoresearch.md
---

# 自主 ML 研究（Autonomous ML Research）

> AI agent 在无人值守的情况下自主进行机器学习实验：修改代码 → 运行实验 → 评估结果 → 迭代改进。

## 核心思想

传统 ML 研究中，研究员手动修改代码、运行实验、分析结果，循环周期慢。自主 ML 研究将这个循环交给 AI agent 自动完成，人类只需：

1. 定义研究目标（写 `program.md`）
2. 启动系统
3. 早上查看实验日志和最优结果

## 关键设计要素

### 1. 明确的 agent 修改边界
agent 只修改一个文件（如 `train.py`），避免副作用，保持 diff 可审查。

### 2. 固定时间预算
每次实验固定时长（如 5 分钟），确保：
- 所有实验在相同条件下可比
- 预测总实验数（12次/小时，~100次/夜）
- 避免长尾实验拖慢整体进度

### 3. 单一优化指标
选择一个与架构无关的指标（如 val_bpb）：
- 简化 agent 决策
- 避免多目标权衡
- 允许跨实验公平比较

### 4. Markdown 编程接口
用 `program.md` 而非代码给 agent 下指令，降低人类的编程门槛，也让指令更自然语言化。

## 与 AI Agent 的关系

自主 ML 研究是 [[ai-agent|AI Agent]] 的一个具体应用领域。agent 在此场景中需要：
- 理解现有代码的结构和意图
- 生成合理的修改假设
- 解析实验结果并决定下一步方向

## 开放问题

- agent 如何避免陷入局部最优（重复类似修改）？
- 如何让 agent 的"直觉"与 ML 领域知识对齐？
- 固定时间预算是否适合所有类型的实验？

## 来源

- [[../../sources/articles/karpathy-autoresearch|karpathy/autoresearch]] — 最具体的开源实现
