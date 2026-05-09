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

## deliverables 结构（2026-05-09 整理，2026-05-09 迁引擎）

- [[projects/2026-05-a-share-quant/deliverables/experiments/|experiments/]] —— 本 project 的 M3/M4 回测 Spike 脚本 + 产物
- [[projects/2026-05-a-share-quant/deliverables/strategy-selection.md|strategy-selection.md]] —— M1 方向选型稳定版
- [[projects/2026-05-a-share-quant/deliverables/m4-strategy-v1.md|m4-strategy-v1.md]] —— M4 H3 固化规格
- [[projects/2026-05-a-share-quant/deliverables/m4-report.md|m4-report.md]] —— M4 官方回测报告

**引擎已迁至 [[practices/quant-investing/README|practices/quant-investing/engine/]]**（2026-05-09），跨 project 共享。本 project 作为"引擎孵化容器"已完成使命，后续 A 股 project 直接从 practices 引用。
