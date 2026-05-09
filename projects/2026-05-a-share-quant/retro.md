---
project: 2026-05-a-share-quant
status: done
created: 2026-05-08
updated: 2026-05-09
---

# A 股量化策略 · 复盘

## [2026-05-09] final 复盘

### 做成了什么

对照 [[brief.md]] 的 5 条目标和 5 个里程碑：

| brief 目标 | 结果 |
|---|---|
| ① 选定 1 类主策略方向并说清理由 | ✓ [[deliverables/strategy-selection.md]]：时序趋势+事件驱动过滤（主方向）/ 小市值多因子（备选）|
| ② 本地数据管道（5+ 年日频 + 财务）| ✓ 超额完成：全市场 5838 只 × 10 年，DuckDB 2.2GB；含健康体检 |
| ③ 回测框架 + 跑出 1 个策略的完整回测 | ✓ 自研引擎 ~330 行 + Spike A→H3 单日跑完 10+ 单变量实验 |
| ④ "加新因子 → 重跑"的闭环工程 | ✓ `strategy(asof, bars, portfolio) -> weights` 协议让每个 Spike 只改 30-100 行 |
| ⑤ 可回流 wiki 的方法论 / 知识卡 | ✓ 本次回流 5 个页面（见下方）|

**里程碑全部勾选**：M1 → M2 → M3 → M4 → M5（本次）。

**规模**：25+ 份文档 / 10+ 张图 / ~3000 行代码 / 1 天完成。

### 没做成 / 改动了什么

**刻意放弃 vs 原计划**：

- **策略未达 brief §六 验收线**（年化 ≥20% / Sharpe ≥0.8 / MDD <35% / Calmar ≥0.8）。H3 四项全不过。但这**不是失败** —— brief §里程碑 M4 只要求"出炉 + 复盘"，没说"过验收"
- **M2b 存储赛道支线未推进到回测**。架构建好了（[[notes/m2b-storage-strategy.md]]），S1/S2 数据源未接入（颗粒价 / 美光海力士）。留给下个 project
- **事件驱动强形式未做**（公告 / 龙虎榜正向打分）。需要补公告文本管道，M5+ 工作

**过程中改动**：

- M3 hello-world 原计划 510300.SH ETF，因为数据未入库临时改茅台 600519.SH；之后补拉 ETF 做了 v2
- M4 方向被 prior-art 调研"颠覆一次"：原计划"Spike B + 4 P0 改造"作废，切到"反转 + 反向闸 + 行业两层 + 多窗合成"

### 关键决策

按"下次还可能遇到"筛选（不是全决策流水账）：

1. **选自研回测引擎而不是 qlib/Backtrader/rqalpha**（M3）
   - 理由：qlib 绑定 ML 训练 + 私有 binary 数据格式；rqalpha 官方无横截面选股示例；Backtrader 停维护
   - 在 M4 Spike G/H 反复改策略时证明正确：每个 Spike 改 30-100 行就能跑
   - 教训：**开源生态里"像能用的"迁移成本经常比自己写高**。调研 §9 的 6 项目可抄性评估证实

2. **Spike 链 = 每次改一个变量**（M4）
   - A→B 改持仓数，B→D 改信号符号，E→F 加行业分散，F→G 加止损，F→H 改残差，H→H3 改多窗
   - 每步改动都有独立归因
   - 如果一个 Spike 改两件事，好坏都说不清来自哪里

3. **调研先行**（Spike 失败后触发）
   - Spike A/B/C 三连跪（-99%）后才去做 prior-art
   - 30 分钟看 BigQuant "IC -0.244" 就能直接跳到反转方向起步
   - 教训：**回测前先问"信号的 IC 符号我知道吗"**

4. **F 不是真最佳**（Spike H 才知道）
   - F 的 +67% 累计里 2016 单年贡献 +51%（熔断 + 整体反弹 = β 运气）
   - H 剥市场 β 后看似跑输，样本外（剔除 2016）其实胜 F
   - 教训：**每个策略必须做 ex-某个极端年的稳定性检查**

5. **M4 收尾 = baseline 固化，不是"过验收"**
   - 用户对齐："策略方向看起来不成功，但作为一次策略尝试，需要充分总结好经验方法"
   - 于是 M4 交付三份：m4-strategy-v1（规格）、m4-report（按验收格式）、m4-retrospective（方法论）
   - brief §里程碑写的是"回测结果出炉 + 复盘"，未说"过验收"

### 可回流到 wiki 的知识

最终选定 **5 条**（宁缺毋滥）：

- **综合** · [[wiki/synthesis/quant-strategy-spike-methodology|量化策略 Spike 开发方法论]] — 7 条模式 + 5 个反直觉发现。本项目最有长期价值的产出
- **概念** · [[wiki/concepts/programming/backtest-engine-defense-checklist|回测引擎防御清单]] — T+1 / 停牌断点 / 复权跳变 / 前瞻偏差四条通用防御规范
- **实体** · [[wiki/entities/products/quant-engine|quant-engine]] — 本项目自研引擎（`strategy(asof, bars, portfolio) -> weights` 协议，~350 行）。下一个 A 股 project 共享
- **实体** · [[wiki/entities/products/tushare-pro|Tushare Pro]] — A 股数据源，通用工具
- **实体** · [[wiki/entities/products/duckdb|DuckDB]] — 嵌入式列存 SQL，本项目首次用

### 不回流的理由

明确**不建 concept 页**的候选：

- **"A 股短期反转 > 动量"** —— 这应当是一个 concept，但按 CLAUDE.md §6.1 概念页要求"跨源综合"。本项目的 4 个外部证据（BigQuant / 清华白颢睿 / 申万 / Zhihu）都没摄入到 `raw/` 变成源摘要页。没有源摘要页就写 concept = 单源综合，违规。**留待未来某次用 wiki-ingest 摄入 prior-art 原文后再建**
- **"A 股反转因子 IC 曲线"**、"T+1 隔夜折价" 等细节 —— 都是单一论文的具体实证结论，不宜泛化为独立 concept
- **M4-v1 策略本身** —— 策略不成功，写成实体卡片意义不大。固化在 `deliverables/m4-strategy-v1.md` 项目内即可
- **项目自身作为 entity**（`wiki/entities/projects/`）—— skill 说"大项目可选"。本项目 retro.md 已完整，再写一张卡片是重复

### 开放问题

留给日后思考：

1. **单因子 α 上限是多少**：H3 Sharpe 0.13 可能就是"月频反转 + 行业分散 + 闸门"的天花板。需要多因子合成才能突破。具体哪些因子组合能过 Sharpe 0.8？
2. **prior-art 摄入流程**：调研查到的 4 篇外部资料（清华白颢睿 / BigQuant / Zhihu / 申万）都值得进 `raw/` 做源摘要页，但本次没做。后续做 a-share-reversal concept 必须先补这块
3. **pipeline 的 progress 漂移 bug**：未定位根因，当前靠 healthcheck 扫描兜底。积累到下次 daily_update 大量异常时再查
4. **下一步路径选择**：两条
   - A 股方向延续 —— 基于 H3 做多因子叠加 或 切备选"小市值多因子"
   - 换方向 —— 美股 / 加密 / ETF 轮动
   - 现状未决

### 产出清单

所有 Spike 详细 results 保留在 [[notes/]]，~25 份。
代码保留在 [[deliverables/data-pipeline/]]（引擎）+ [[deliverables/experiments/]]（实验）。
核心交付：
- [[deliverables/strategy-selection.md|strategy-selection]]（M1）
- [[deliverables/m4-strategy-v1.md|m4-strategy-v1]]（M4 H3 固化规格）
- [[deliverables/m4-report.md|m4-report]]（按验收线格式）
- [[notes/m4-retrospective.md|m4-retrospective]]（方法论详细版，本次回流的原始素材）
- [[notes/m4-prior-art.md|m4-prior-art]]（外部调研，尚未沉淀为 wiki sources）
