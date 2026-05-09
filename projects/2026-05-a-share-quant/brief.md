---
project: 2026-05-a-share-quant
status: active
created: 2026-05-08
updated: 2026-05-09
---

# A 股量化策略 · 简报

## 背景
对 A 股市场的量化策略有实操兴趣。目前无已有策略、无实盘账户、无数据管道。想系统性地走一遍"选方向 → 搭数据 → 写回测 → 出策略 → 走向实盘"的全链路，而不是停留在读论文/看公众号的阶段。

## 目标
项目结束时达到以下状态：
1. 已经选定 1 类主策略方向（如多因子选股 / 趋势跟随 / 统计套利 / 事件驱动），并能用一段话说清楚选型理由与预期收益风险特征。
2. 有一套可运行的本地数据管道，能获取 A 股日频（至少）行情 + 基础财务数据，并稳定地供回测使用。
3. 有一个可跑通的回测框架（自研或开源封装），并用它完整跑出至少 1 个候选策略在近 N 年的回测结果（含净值曲线、收益/回撤/胜率等核心指标）。
4. 对所选策略写成可迭代的代码工程，具备"加入新因子/新规则 → 重跑回测"的闭环。
5. 沉淀出一套可回流到 wiki 的方法论与知识卡（因子定义、回测陷阱、选型框架等）。

## 非目标
- **不做** 高频 / tick 级策略（数据与基础设施成本过高，偏离当前阶段）。
- **不做** 期货、期权、数字货币等非 A 股标的（本项目名字已划定范围）。
- **不做** 机器学习/深度学习驱动的黑箱策略作为主线（可作为后续分支，但首版要求可解释）。
- **不做** 完整的交易执行系统（如券商接入、风控引擎），只做到"离实盘一步之遥"。
- **不**在本项目里解决资金管理、税务、合规等账户层面问题。

## 范围
包含：
- 主流 A 股量化策略思路的调研与选型（因子、趋势、套利、事件等）
- 本地数据管道搭建（数据源评估、接入、清洗、存储、增量更新）
- 回测框架的选型或自研（Backtrader / vnpy / qlib / zipline-cn / 自写 等对比）
- 选定策略的代码实现、参数回测、结果分析
- 与策略相关的风险/回测陷阱/评价指标笔记
- 关键概念/工具/方法论向 wiki 的知识回流

不包含：见"非目标"。

## 交付物
- [x] **调研综述**：[[projects/2026-05-a-share-quant/deliverables/strategy-selection.md|strategy-selection.md]] + [[projects/2026-05-a-share-quant/notes/m4-prior-art.md|m4-prior-art.md]]
- [x] **数据管道**：[[projects/2026-05-a-share-quant/deliverables/data-pipeline/|data-pipeline/]]（引擎可跨 project 共享）
- [x] **回测代码**：[[projects/2026-05-a-share-quant/deliverables/data-pipeline/|data-pipeline/]]（backtest/ 引擎）+ [[projects/2026-05-a-share-quant/deliverables/experiments/|experiments/]] scripts/data
- [x] **策略 v1 固化**：[[projects/2026-05-a-share-quant/deliverables/m4-strategy-v1.md|m4-strategy-v1.md]]
- [x] **M4 回测报告**：[[projects/2026-05-a-share-quant/deliverables/m4-report.md|m4-report.md]]
- [x] **策略笔记/知识卡**：notes/ 下 20+ 份 M1-M4 Spike 文档 → M5 回流 wiki

## 里程碑
- [x] M1 · 方向选型完成 — 2026-05-08 实际完成（见 [[projects/2026-05-a-share-quant/deliverables/strategy-selection.md|strategy-selection]]）
- [x] M2 · 数据管道跑通（能取到至少 5 年日频数据 + 基础财务） — 2026-05-09 实际完成（全市场 5838 只 × 10 年，daily_bar 1063 万行 / adj_factor 1105 万行 / daily_basic 1055 万行 / fina_indicator 11.2 万行；DuckDB 2.2 GB）
- [x] M3 · 回测框架选定并跑通 hello-world 策略 — 2026-05-09 实际完成（自研引擎 ~330 行；茅台 SMA(20/60) 跑通 10 年 2509 交易日，年化 +16.18% / MDD -41% / Sharpe 0.67；见 [[projects/2026-05-a-share-quant/notes/m3-hello-world.md|m3-hello-world]]）
- [x] M4 · 首个候选策略回测结果出炉 + 复盘 — 2026-05-09 实际完成（Spike A→H3 单日跑完 10+ 个单变量实验；最终 baseline = H3 多窗残差反转 + 行业两层 + 反向闸；累计 +52.83% / 10Y / Sharpe 0.13，**跑赢 HS300 +12.83pp 但不达 brief §六 验收线**；交付 [[projects/2026-05-a-share-quant/deliverables/m4-strategy-v1.md|m4-strategy-v1]] / [[projects/2026-05-a-share-quant/deliverables/m4-report.md|m4-report]] / [[projects/2026-05-a-share-quant/notes/m4-retrospective.md|m4-retrospective]]）
- [x] M5 · 阶段复盘 + 知识回流 wiki — 2026-05-09 实际完成（retro.md 填写 final 复盘；5 条回流：synthesis/quant-strategy-spike-methodology + concepts/programming/backtest-engine-defense-checklist + entities/products/{quant-engine,tushare-pro,duckdb}；README status=done）

## 风险 / 未知
- **数据质量**：A 股免费数据源（Tushare / AkShare / Baostock 等）在停复牌、分红除权、财报修正上的坑尚未评估。
- **幸存者偏差 / 未来函数**：回测中极易引入，需要在框架层就防住，而不是事后发现。
- **策略容量与可行性**：回测跑出漂亮曲线 ≠ 实盘可行，需提前考虑交易成本、滑点、流动性。
- **精力投入节奏**：项目跨度大（≥ 2 个月），容易被打断；里程碑粒度要控制住，避免中断后拾不回来。
- **回测框架选型**：自研 vs 用开源（qlib / Backtrader），尚未评估学习/维护成本，是早期关键决策点。
- **非目标边界漂移**：过程中容易被 ML/期货/实盘执行等方向吸引，需要 brief 本身作为锚。
