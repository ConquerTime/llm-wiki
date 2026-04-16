---
title: "karpathy/autoresearch — 自主 ML 研究框架"
type: source
subtype: github
tags: [ai-agent, ml-research, autonomous, karpathy]
created: 2026-04-16
updated: 2026-04-16
sources:
  - ../../../raw/articles/karpathy-autoresearch.md
author: Andrej Karpathy
url: https://github.com/karpathy/autoresearch
date: 2026-04
---

# karpathy/autoresearch — 自主 ML 研究框架

> Karpathy 的实验性框架：让 AI agent 在一夜之间自主运行 ~100 次 ML 实验，早上醒来看结果。

## 核心摘要

AutoResearch 让 AI agent 自主进行机器学习研究：修改训练代码 → 运行实验 → 评估结果 → 循环迭代，无需人类干预。其设计哲学是**极简主义**：3 个文件、1 个指标、固定时间预算。

## 关键要点

1. **三文件架构**：`prepare.py`（只读工具）、`train.py`（agent 的唯一修改目标）、`program.md`（人类给 agent 的指令）
2. **固定时间预算**：每次实验恰好 5 分钟，与硬件无关，一夜可跑 ~100 次实验
3. **单一指标**：val_bpb（验证集 bits-per-byte），与词汇表大小无关，允许跨架构公平比较
4. **Agent 修改范围**：架构、超参数、batch size、优化器（Muon + AdamW）——几乎任何 train.py 内容
5. **人类编程接口**：用 `program.md` 这个 markdown 文件指挥 agent，而非直接写 Python
6. **自包含设计**：仅依赖 PyTorch，单 GPU，不需要分布式训练

## 关键摘录

> "Users wake up to a log of experiments and an optimized model."

> "Rather than manually editing Python files, researchers program `program.md` markdown files that instruct autonomous agents."

> "All training runs execute for exactly 5 minutes of wall-clock time, independent of compute specifications."

## 涉及概念

- [[../../concepts/ai/ai-agent|AI Agent]] — autoresearch 是 agent 自主研究的具体实现
- [[../../concepts/ai/autonomous-research|自主 ML 研究]] — 新概念，本仓库是代表案例

## 涉及实体

- [[../../entities/persons/andrej-karpathy|Andrej Karpathy]] — 作者
- [[../../entities/products/autoresearch|autoresearch]] — 本项目
