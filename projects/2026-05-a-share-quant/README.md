---
project: 2026-05-a-share-quant
status: done
created: 2026-05-08
updated: 2026-05-09
---

# A 股量化策略

> 面向 A 股的量化策略研究与实盘开发：打通数据管道，落地至少一个可回测、可迭代至实盘的策略。

✅ **已完成于 2026-05-09**，见 [[projects/2026-05-a-share-quant/retro.md|retro.md]]。
策略不达 brief §六 验收线，但产出可复用引擎 + 方法论 5 条已回流 wiki。

- **状态**：done
- **简报**：[[projects/2026-05-a-share-quant/brief.md|brief]]
- **日志**：[[projects/2026-05-a-share-quant/log.md|log]]
- **复盘**：[[projects/2026-05-a-share-quant/retro.md|retro]]
- **外部关联**：无（纯新起）

## deliverables 结构（2026-05-09 整理）

- [[projects/2026-05-a-share-quant/deliverables/data-pipeline/|data-pipeline/]] —— **引擎**（数据管道 + 回测引擎 + 因子 + 样本池）。可跨 project 复用
- [[projects/2026-05-a-share-quant/deliverables/experiments/|experiments/]] —— 本 project 的 M3/M4 回测 Spike 脚本 + 产物
- [[projects/2026-05-a-share-quant/deliverables/strategy-selection.md|strategy-selection.md]] —— M1 方向选型稳定版

下一个 A 股策略项目启动时，从 `data-pipeline/` 共享引擎（path install），各自在自己的 `experiments/` 里跑实验。
