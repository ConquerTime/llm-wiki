---
title: autoresearch
type: entity
subtype: product
tags: [karpathy, ai-agent, ml-research, github]
created: 2026-04-16
updated: 2026-04-16
sources:
  - ../../../raw/articles/karpathy-autoresearch.md
---

# autoresearch

> Karpathy 开发的实验性框架，让 AI agent 在单 GPU 上一夜自主运行 ~100 次 ML 实验。

## 基本信息

- **作者**：[[andrej-karpathy|Andrej Karpathy]]
- **仓库**：https://github.com/karpathy/autoresearch
- **许可**：MIT
- **状态**：实验性

## 与本 wiki 的关联

- 极简三文件设计（prepare.py / train.py / program.md）的代表案例
- 用 markdown 文件（program.md）作为人类→agent 的编程接口
- 固定时间预算（5分钟/次）使实验结果跨硬件可比较
- 单一指标（val_bpb）让 agent 聚焦目标

## 出现在

- [[../../sources/articles/karpathy-autoresearch|karpathy/autoresearch 源摘要]] — 主要来源
