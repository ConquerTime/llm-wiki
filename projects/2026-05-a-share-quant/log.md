# A 股量化策略 · 活动日志

> 追加式时间线，记录讨论、决策、产出、阻塞。

---

## [2026-05-08] 启动
- 项目创建，目录初始化（raw/ notes/ deliverables/）
- 与用户对齐：
  - 核心目标 = 实盘策略开发（非纯研究、非纯学习）
  - 交付物 = 数据管道 + 可跑回测代码 + 综述文档 + 策略笔记
  - 短名 = a-share-quant（英文，宽泛，便于长期使用）
  - 外部关联 = 无，纯新起
- 非目标已写入 brief：不做高频、不做非 A 股、不做黑箱 ML 主线、不做完整执行系统
- 下一步：M1 方向选型，先做策略思路调研

## [2026-05-08] M1 方向选型 · 进行中
- 对齐个人画像：100–500 万 / 盘中高频关注 / 进攻型年化 30%+ 容忍 30% 回撤 / 无方向倾向
- 产出约束锚点：[[projects/2026-05-a-share-quant/notes/m1-constraints.md|m1-constraints]]
- 产出策略家族调研：[[projects/2026-05-a-share-quant/notes/m1-strategy-families.md|m1-strategy-families]]
- **推荐主方向**：时序趋势 / 动量 + 事件驱动过滤器
- **备选方向**：小市值多因子（进攻版，仅主方向失败时启用）
- 明确排除：均值回归、统计套利（做空受限）、纯打板（监管 + 盯盘质量）
- 待用户确认：主方向选型是否采纳；采纳后升级到 deliverables/strategy-selection.md

## [2026-05-08] M2 数据管道 · 骨架落地
- 决策对齐：Tushare Pro 主 + AkShare 补 / DuckDB / 10 年全市场 / Python 3.11 + uv
- 决策记录：[[projects/2026-05-a-share-quant/notes/m2-decisions.md|m2-decisions]]
- 代码骨架：`deliverables/data-pipeline/`
  - `quant_data/sources/` tushare + akshare adapter（拉数）
  - `quant_data/storage/duckdb_store.py` DuckDB schema + 幂等 upsert + 进度表
  - `quant_data/ingest/` 日线 + 复权 + 每日基础 + 财务的增量编排
  - `quant_data/api.py` 统一读数 API（含前复权动态计算、ann_date 防前瞻）
  - `scripts/bootstrap.py` + `scripts/daily_update.py`
  - `README.md` 使用说明
- 所有 Python 文件语法检查通过
- 待用户：注册 Tushare Pro 账号、配置 TUSHARE_TOKEN，跑 `--smoke` 验证通路

## [2026-05-08] M2 · 冒烟测试通过 + 全量拉数启动
- Tushare token 配置完成（2000 积分账号）
- 修复 4 个 bug：
  1. dotenv 按 cwd 找不到 .env → 改为显式指向 `PIPELINE_ROOT/.env`
  2. DuckDB 把 `CURRENT_TIMESTAMP` 误识别为列名 → 改用 `now()`
  3. Tushare `fina_indicator` 同季度多公告导致主键冲突 → 入库前按 ann_date 去重保留最新
  4. DuckDB `CAST('19910403' AS DATE)` 不支持 YYYYMMDD → 改用 `strptime(list_date, '%Y%m%d')`
- 冒烟测试 5 只股票全通过：
  - daily_bar 11782 行、adj_factor 11957 行、daily_basic 11782 行、fina_indicator 204 行
  - 幂等性验证：二次跑 0 重拉
  - 前复权验证：茅台 2025-04 末 qfq 1494.76 vs raw 1550（合理除权差）
  - 2024 年交易日 242 天（与官方一致）
  - 财务 as_of_date 防前瞻验证通过
- **全量拉数已在后台启动**（PID 22474，日志 `data/bootstrap.log`）
- 预计耗时 ~3 小时（5838 只 × ~1.5s + 财务）
- 拉完后进 M3

## [2026-05-08] M1 闭环 · 策略选型稳定版上线
- 稳定版交付：[[projects/2026-05-a-share-quant/deliverables/strategy-selection.md|strategy-selection]]
- 主方向：时序趋势 / 动量 + 事件驱动过滤器（纯多头）
- 备选方向：小市值多因子（进攻版，仅主方向失败时启用）
- 评价标准（M4 验收用）：年化 ≥20% / Sharpe ≥0.8 / MDD <35% / Calmar ≥0.8
- 样本期硬性要求：必须覆盖 2018 熊市 + 2021 风格切换 + 2024.1
- 实盘打折惯例：实盘年化 = 回测 × 0.75
- brief.md M1 里程碑勾选

## [2026-05-08] 价投线 · 纪律框架草稿
- 用户承认实盘持仓存在纪律问题（卖飞光模块 FOMO、100% 单赛道、无止损）
- 当前持仓：德明利 70% + 江波龙 30%，全仓存储模组
- 核心争议锁定："低价存货用完后能不能继续赚" = 三情景模型（周期见顶/议价传导/量增抵消）
- 产出纪律框架草稿：[[projects/2026-05-a-share-quant/notes/m1-holdings-discipline.md|m1-holdings-discipline]]
  - 仓位上限（单票 ≤30% / 单赛道 ≤60% / 现金 ≥20%）
  - 三层止盈（阶梯 / 基本面 / 技术）
  - 止损阶梯（-15% / -25% / -35%）
  - 反情绪机制（光模块遗憾隔离 / 3 天冷却 / 月度复盘）
- 待 bootstrap 完成后：拉德明利+江波龙全历史数据，按 6 项指标做数据体检
- 用户决策：数据核验后再决定降仓幅度 + 是否启动 holdings-tracker 子项目
- 待确认：两只股票的 Tushare ts_code

## [2026-05-08] 数据体检完成 · 持仓三维分析
- 确认持仓标的：德明利 001309.SZ / 江波龙 301308.SZ（均 2022 年上市，样本 ~11 季）
- 产出数据体检报告：[[projects/2026-05-a-share-quant/notes/m1-holdings-checkup.md|m1-holdings-checkup]]
- 关键发现：
  - 2026Q1 毛利率 57%/55%（历史峰值）、净利率 44%/40% —— 真实主业驱动，无一次性损益
  - **但**一季度内存货暴增 +51 亿 / +63 亿，借款暴增 +14 亿 / +60 亿
  - 经营现金流连续深红 —— 账面赚 30 亿，现金净流出
  - 财务特征 = 杠杆周期股见顶区教科书形态
  - 股价近 1 年 +553% / +504%，基本在历史最高
  - 估值 PS 93%/98% 分位 + 市值已达 1356 亿 / 2012 亿（准半导体龙头级）
- 概率加权期望值（A 乐观/B 中性/C 悲观 = 25/45/30）：
  - 德明利 -13.3% / 江波龙 -27.7% / 佰维 -25%
- 同步拉取对照组数据：
  - 光模块三家（中际旭创/新易盛/天孚通信）：毛利率稳定 +5pp、零借款、经营现金流大正
  - 企业级存储（澜起/深科技/兆易/东芯/北君）：财务健康度显著高于模组三家
- 与用户讨论得出：光模块 ≠ 模组厂本质，存储赛道内部需要按"AI 纯度 + 财务健康"分层

## [2026-05-08] M2-branch 立项 · 存储赛道主题量化策略
- 用户命题：假设 100 万满仓存储，收益最大化 + 择时 + 大方向反转清仓
- 立项为沙盘推演（**非实盘计划**），作为主线 M3/M4 的第二条量化支线
- 产出：
  - 策略设计：[[projects/2026-05-a-share-quant/notes/m2b-storage-strategy.md|m2b-storage-strategy]]
  - 支线简报：[[projects/2026-05-a-share-quant/notes/m2b-brief.md|m2b-brief]]
  - 存储池定义：`deliverables/data-pipeline/quant_data/universe/storage.yaml`（8 只标的 × 3 档配置）
- 核心设计：
  - 三档静态配置（激进 A / 均衡 B / 防御 C）
  - 四信号共振打分（颗粒 S1 / 原厂 S2 / 财务 S3 / 技术 S4，范围 -24 到 +16）
  - 得分 → 仓位映射表（7 档从清仓到满仓）
  - 月度内部轮动（前 3 +50%、后 2 -30%）
  - 硬清仓 R1-R6 + 软减仓缓冲 + Phase 4 终极退出
- 当前信号估算：综合 +14 → 满仓配置 A（但意识到"所有好消息已被确认"的敏感区）
- 下一步：
  - M2b-2（本月底）：实现 S3/S4 打分器代码（可用现有数据）
  - M2b-3（6 月）：补 S1 颗粒价、S2 美光/海力士数据源
  - M2b-4（7 月）：依赖主线 M3 回测框架完成
- 回测目标：年化 ≥50% / 最大回撤 ≤35% / Sharpe ≥1.2

## [2026-05-09] M2 数据管道 · 全量拉数完成
- bootstrap 全量跑完（约 39 分钟财务 + 前序日线，单轮无中断）
- 最终数据库状态：
  - stock_basic 5,838 行
  - trade_cal 3,781 行
  - daily_bar 10,631,843 行
  - adj_factor 11,047,477 行
  - daily_basic 10,548,595 行
  - fina_indicator 111,608 行
  - ingest_progress 17,219 行
  - DuckDB 文件 2,206.51 MB
- brief.md M2 里程碑勾选
- 下一步：先做 M2 数据体检再进 M3

## [2026-05-09] M2 数据体检 · 完成
- 脚本：`deliverables/data-pipeline/scripts/healthcheck.py`（只读，7 项检查）
- 报告：[[m2-data-healthcheck|m2-data-healthcheck]]
- 初判 4 fail / 3 pass；经分组诊断后**全部降级**，数据可用于 M3
  - 项 1 · 覆盖：100 → 11（89 只 2016 前退市，合理）；剩 11 只 active 但无日线（P1 修）
  - 项 2 · 交易日：154 → 0（4000 阈值错，2020 前 A 股上市数本就 < 4000）
  - 项 3 · 财务稀疏：2506 只无 fina_indicator（Tushare 2000 积分覆盖限制，P2）
  - 项 5 · 复权：2543 → 158（BJ 2385 行是北交所 adj quirk；沪深 158 行是真 gap）
  - 项 4/6/7 干净通过
- **M3 框架层必须防住的 4 条**：样本池剔除规则 / 停牌断点 / 复权跳变标 suspect / 财务前瞻用 ann_date
- 下一步：
  - P1 修：11 只 active 无日线（怀疑是 bootstrap start_date 过滤问题）
  - 进 M3 · 回测框架选型

## [2026-05-09] M3 · 回测框架选定 + hello-world 跑通
- 决策对齐：自研轻量引擎（淘汰 Backtrader 停维护 / qlib 过重 / bt 无 A 股适配）
- 决策记录：[[projects/2026-05-a-share-quant/notes/m3-decisions.md|m3-decisions]]
- Hello-world 标的切换：原计划 510300.SH 沪深 300 ETF 不在库，临时改 600519.SH 茅台
- 引擎落地：`quant_data/backtest/`
  - `engine.py` 240 行：T+1 开盘成交 / 停牌冻结 / suspect 日扫描 / 手续费模型
  - `metrics.py` 90 行：6 项指标 + 基准比较 + 格式化报告
  - `__init__.py` 入口
- Hello-world 脚本：`scripts/hello_world.py`
- 首跑结果（茅台 SMA(20/60) 10 年 2509 日）：
  - 策略：+345% / 年化 +16.18% / Sharpe 0.67 / MDD -41.01% / 换手 5.10x / 61 笔
  - 基准（买入持有同标的）：年化 +23.19% / MDD -47.02%
  - 超额 -7.01%（预期：双均线在单边牛股跑输，但减了回撤）
- 修了 1 个 bug：metrics.turnover 分母误用归一化 nav → 改为绝对 equity 序列
- NAV 曲线图：`notes/m3-hello-world-nav.png`
- 报告：[[projects/2026-05-a-share-quant/notes/m3-hello-world.md|m3-hello-world]]
- brief.md M3 里程碑勾选
- **"加因子 → 重跑"闭环已建立**：后续加新规则只改 strategy 函数，引擎不动
- 下一步：
  - M4 主线：实现 strategy-selection 定的"时序趋势/动量 + 事件驱动过滤"
  - 补拉 ETF/指数数据（M4 基准要用沪深 300）
  - 并行 M2b 用引擎跑 S3/S4 打分器

## [2026-05-09] P1 数据修补 + ETF/指数入库 + hello-world v2
**P1 · 13 只 active 无日线修复**
- 根因：Tushare 首次拉取返回空 df 时，`update_progress` 仍被更新，导致幂等跑不会重试
- 覆盖范围：11 只（601138 工业富联 / 601155 新城 / 300450 先导智能 等）+ 2 只 daily_ingest_errors 里的
- 修复方式：直接调 upsert 绕过 `_decide_start`；验证 13 只全部 daily_bar/adj_factor/daily_basic 齐备
- 待修 pipeline bug（不阻塞 M4）：ingest 空 df → 记 errors csv 而非静默更新进度

**基准数据入库**
- tushare adapter 新增 `fetch_index_daily` + `fetch_fund_daily`
- 一次性脚本：`scripts/ingest_benchmarks.py`
- 入库：000300.SH 沪深 300 指数 2510 行 + 510300.SH 华泰柏瑞 ETF 2510 行（都进 daily_bar 表）
- 简化：不入 adj_factor（指数无复权；ETF 分红小，v2 忽略）

**Hello-world v2 跑通**
- 510300 SMA(20/60)：累计 -7.73% / 年化 -0.80% / Sharpe -0.22 / MDD -41.62% / **交易 671 次**
- 对比茅台：+302% / +15% / Sharpe 0.62 / 交易 55 次
- ETF 买入持有 ≈ 指数基准（年化 3.50% vs 3.47%）→ 验证 ETF 跟踪质量 + 引擎 NAV 正确
- NAV 图：`notes/m3-hello-world-v2-nav.png`
- 报告：[[projects/2026-05-a-share-quant/notes/m3-hello-world-v2.md|m3-hello-world-v2]]

**给 M4 的明确证据**
- 双均线在沪深 300 震荡结构里被切片 → "时序趋势 + 事件驱动过滤"里**事件过滤不是可选**，是必须
- 事件过滤器的本质 = 只在"方向存在"的时段开仓

**小改进清单（M4 前可做）**
- pipeline: 空 df 记 errors，不静默
- pipeline: update_progress 只在 upsert > 0 行时触发
- backtest: 支持"基准从另一 ts_code 读"（M4 必须）

**下一步：M4 主线**

## [2026-05-09] 引擎 Bug 2 修复 · 支持跨标基准
- 用户决策：Bug 1 根因未定位（静默进度漂移），不推测性修复；只修 Bug 2
- Bug 2：引擎基准只能是同标 buy&hold，M4 需要"策略跑 X 基准画 Y"
- 修改（简单优先，不动引擎）：
  - `backtest/metrics.py` 新增 `buy_and_hold_nav(bars_df)` 工具：bars → 归一化 NAV Series
  - `backtest/__init__.py` 导出
  - `scripts/hello_world.py` 加 `--benchmark` / `--benchmark-adj` / `--adj` 参数
- 三 case 验证：
  - case 1 默认（茅台同标 buy&hold）：年化 +16.18% vs +23.19%，超额 -7.01%（与 v1 一致）
  - case 2 跨标（茅台 vs HS300 指数）：超额 **+12.71%**（符合茅台 10 年跑赢大盘）
  - case 3 ETF vs HS300 指数：超额 -4.27%（接近 0，验证 ETF 跟踪指数质量）
- Bug 1 留档未修：pipeline 的 `update_progress` 漂移，等 daily_update 再次暴露时再定位根因
- **M3 完全就绪，进 M4**

## [2026-05-09] M4 Spike · 两种纯动量形态对比
**决策（3 个 AskUserQuestion）**
- 形态：两种都跑一版对比后再定（Spike A 单票 Top1 / Spike B 横截面 Top10 月频）
- 主信号：回看窗动量（20 日）
- 事件过滤：仅用现有数据做负过滤（ST / 停牌 / 成交额末 20% / 上市 <250 日 / 北交所）

**产出**
- 规格：[[projects/2026-05-a-share-quant/notes/m4-spike-spec.md|m4-spike-spec]]
- 结果：[[projects/2026-05-a-share-quant/notes/m4-spike-results.md|m4-spike-results]]
- 新模块：`quant_data/universe/`（负过滤）+ `quant_data/factors/momentum.py`
- 协调器：`scripts/m4_spike.py`
- 引擎扩展：`fast_mode` 参数（不切片 bars_hist，适合全市场扫描）

**修了 2 个真 bug**（不影响 hello-world）
1. `build_universe`：trade_cal 只覆盖 2016+，导致 list_idx 全 0、250 日门槛无法满足。改用日历日计算
2. `engine._execute_orders`：prices dict 只含 target_weights，导致换标的时老持仓无法卖出。改为 `target ∪ holdings`

**性能**：全市场 1060 万行 DuckDB 3.5s 拉完，单次回测 ~140s

**结果（惨烈但有明确结论）**
- Spike A Top1 日频：**-99.95%** / Sharpe -1.02 / MDD -99.96% / 637 笔
- Spike B Top10 月频：**-99.10%** / Sharpe -1.28 / MDD -99.17% / 2945 笔
- 基准 HS300：+40% / 年化 +3.47% / MDD -45.60%

**诊断出三个结构性陷阱**（非 bug）
1. A 股动量反转效应：Top 20 日涨幅股 = 冲高回落前的峰值
2. 次新股污染：250 日门槛不够，IPO 后 300-500 日的妖股大量进入候选
3. T+1 + 月频反应迟钝：信号错了等一个月时已经腰斩

**Spike 证伪了"裸动量 Top K"，没证伪"趋势 + 过滤"**

**M4 正式版修改清单（按 strategy-selection §3.3 M4 设计补回）**
- ATR 止损、大盘趋势闸（HS300 > SMA60）、涨停日不买入、次新窗口扩 500、动量去一日脉冲
- 底座选 Spike B（Top K 月频），改造后再做

**下一步**
- 启动 M4 正式版
- 或先做大盘趋势闸单项回测看效果
- 或切备选小市值多因子

## [2026-05-09] M4 Spike C · 大盘趋势闸单变量对照
**设计**：Spike B 原样 + 一条闸门 `HS300.close > SMA60 才开仓，否则立即空仓`
- 闸门开仓时间占比：52.63%（10 年约一半）
- 新增 `make_spike_c_strategy` ~40 行，`prepare_data` 加 HS300 趋势信号
- `m4_spike.py` 的 --which 扩为 A/B/C/both/BC

**结果对比**
| | B（裸）| C（+闸门）| HS300 |
|---|---|---|---|
| 累计 | -99.10% | **-96.35%** | +40% |
| 年化 | -37.67% | -28.28% | +3.47% |
| MDD | -99.17% | **-96.95%** | -45.60% |
| Sharpe | -1.28 | **-1.09** | — |
| 换手 | 23.1x | 16.4x | — |

**核心结论：闸门确有改善但救不活**
- 挽回约 9 个百分点年化损失 / MDD 浅 2 pp / 换手降 30%
- 但绝对量级仍在 -96%+，量变没到质变
- 根本原因：闸门只降低"空头段暴露损失"，多头段选出的 Top 10 本身就亏
- 复合效应下 "暴露一半 × 每次暴露都亏" ≠ "不亏"

**对 M4 方向的修正（关键）**：趋势闸不是关键变量，必须在**选股层**动刀。正确 M4 四 P0 改造：
1. 涨停日不买入（剪"买在烟花顶"）
2. 动量信号 = mom_20 - mom_1（剔当日涨停脉冲贡献）
3. 次新窗口扩 500 日（剪 IPO 后妖股爆炒阶段）
4. ATR 止损（单票小回撤即出，避免 -99% 单票事故）

趋势闸降为 P1，**锦上添花不救命**。

**Spike 阶段结束**：三个 Spike (A -99.95 / B -99.10 / C -96.35) 形成完整证据链
- 共同结论：必须在选股层动刀，不能靠外加闸门救
- 图：[[projects/2026-05-a-share-quant/notes/m4-spike-c-gate.png]]
- 报告追加 §10：[[projects/2026-05-a-share-quant/notes/m4-spike-results.md|m4-spike-results]]

**下一步：M4 正式版按 4 项 P0 改造 Spike B**

## [2026-05-09] M4 Prior-Art 调研 · 方向颠覆
**启动前调研**：M4 正式版前做学术 / 开源 / 社区三方向调研（三 Agent 并行 + wiki-query）
- 产出：[[projects/2026-05-a-share-quant/notes/m4-prior-art.md|m4-prior-art]]
- wiki 查询：a-share-quant 是本项目 wiki 的首批量化知识起点，仅 TradingAgents 一条沾边（多智能体 LLM 交易，不参考）

**核心颠覆发现：A 股 ≤1 月截面是反转不是动量**
- BigQuant 2015-2025 全 A 实测：20 日动量 IC **-0.032** / ICIR **-0.244** / 多空年化 **-6.80%**
- 清华白颢睿 2020：T+1 造成日内动量 vs 隔夜反转相互抵消，月频取到净零区
- Zhihu 反转因子：过去 1 月收益率**取负**做因子，ICIR **2.65**
- 申万宏源：全市场裸涨幅排序 = "反转组"空头 = 必亏
- 聚宽社区案例：行业动量 → 行业内选股两层结构，MDD 13%

**Spike 再诊断**
- 不是"裸动量失败"，是**方向错了**
- mom_20 做多 Top 10 = 在 ICIR -0.244 信号上做多
- 理论年化 -8% × 10 年复利 ≈ -57%，实跑 -99% 的 40pp 差距来自手续费 + 次新样本 + T+1
- **信号取反号就能把 ICIR 由 -0.244 翻为 +0.244**，不需要任何其他改造

**Spike 阶段定的"4 个 P0 改造"作废**
候选 1 · 反转版 Top-K（~30 行）：Spike B 的 nlargest → nsmallest
候选 2 · 残差动量 3-6 月（~100 行）：剥离市场+行业 beta
候选 3 · 行业动量 + 行业内选股（~200 行，聚宽路线）
候选 4 · 多因子合成（~400 行，M5+ 再说）

**推荐路径**：候选 1 → 候选 3
- 先跑候选 1 验证"反号=正收益"
- 若年化 >10% → 推进候选 3 冲击验收线（年化 ≥20% / Sharpe ≥0.8）

**开源可抄清单**（自研引擎，不拖 qlib 依赖）
- qlib Alpha158 的 /$close 归一化约定
- qlib `is_stock_tradable` 三段式（suspended / limit / direction）
- qlib TopkDropoutStrategy 的"不补位"原则
- hugo2046/QuantsPlaybook 的 ATR / 波动率止损代码

**下一步：先跑候选 1（反转版 Spike D）**

## [2026-05-09] M4 Prior-Art 追加 · 开源策略可抄性评估
**问题**：开源策略可以抄吗？它们用什么引擎？
**结论**：6 个项目一个都不能直接抄

- qlib (42k, MIT)：benchmark 全是 ML 打分，**没反转策略**，绑私有 binary
- rqalpha (6.4k)：examples **全是 CTA 择时**，没横截面
- hugo2046/QuantsPlaybook (5k)：**全是因子研究 notebook**，无 backtest 循环
- phonegapX/alphasickle：指数增强 + LP 优化，不是排名选股
- qstock `MR_Strategy`：名字骗人，是**单票**均值回归不是截面反转
- OSkhQuant：CC BY-NC 禁商用 + miniQMT 依赖 → 弃

**三个陷阱**
- qlib 迷惑性最大：benchmark 是线性组合打分不是反转
- qstock `MR_Strategy` 名字像但实际单票择时
- rqalpha 6.4k stars 像生产级但 API 不兼容我的 strategy 协议

**可抄的**
- WorldQuant 101 Alphas 的公式（~10 行/个）
- hugo2046 的两份研报 PDF：《A 股反转之力的微观来源》《再论动量因子》
- qlib `is_stock_tradable` 三段式过滤
- qstock `trade_performance()` NAV/指标代码

**M3 自研引擎决策再次验证**
- 我的 350 行引擎在开源生态里是独一份（`strategy(asof, bars, portfolio) -> weights` 协议）
- 开源项目的引擎和策略耦合紧，想抄策略必须吞整个引擎
- 迁移成本 > 重写

**→ 继续走自研，候选 1（Spike B nsmallest）**。开源作为公式来源，不作框架依赖。
追加到 [[projects/2026-05-a-share-quant/notes/m4-prior-art.md|m4-prior-art]] §9。

## [2026-05-09] M4 Spike D · 反转版跑通
**改动极小**：Spike B 的 `nlargest → nsmallest` + `mom > 0 → mom < 0`，~30 行
- 报告：[[projects/2026-05-a-share-quant/notes/m4-spike-d-results.md|m4-spike-d-results]]

**整体指标**
| | Spike B（动量）| Spike C（B+闸门）| **D（反转）** | HS300 |
|---|---|---|---|---|
| 累计 | -99.10% | -96.35% | **-39.45%** | +40% |
| 年化 | -37.67% | -28.28% | **-4.91%** | +3.47% |
| MDD | -99.17% | -96.95% | **-77.90%** | -45.60% |
| Sharpe | -1.28 | -1.09 | **-0.21** | — |

"反号 = 正收益"假设没兑现。但比 B/C 少亏 60pp，方向对了。

**年度拆分（关键发现）**
- **4/4 胜**：2016 (+8.34%) / 2021 (+23.28%) / 2022 (-8.44% vs -21.27%) / 2025 (+34.18%) — 震荡/风格切换年
- **4/4 败**：2017 (-41.78%) / 2019 (-2.11%) / 2020 (+5.47% 但跑输) / 2024 (-2.22%) — 单边牛市年

**完美印证 BigQuant 报告**：震荡市 ICIR +0.45，牛市 -0.36。

**主要亏损源分解**
- 2017 漂亮 50 单边牛 -41.78% 贡献最大下跌段
- 2018 熊市 -34.62% 接力
- 手续费 10.9 万（换手 26.1x，月频 Top10 换了 8915 笔）

**下一步：候选 1.5（反转 + 反向趋势闸）**
- Spike C 闸门反过来：HS300 < SMA60（震荡/熊）时开仓，> SMA60（单边牛）时空仓
- 改动 ~5 行
- 预期屏蔽 2017/2019/2020/2024 的大部分亏损 → 年化转正
- 若翻不过来，说明裸反转信号本身不够，必须上候选 2（残差反转）或候选 3（行业两层）

## [2026-05-09] M4 Spike E · 反转 + 反向闸门 · 首次翻正
**改动 5 行**：Spike D 加开头 4 行闸门（`if regime_on: 空仓`），反向于 Spike C
- 报告：[[projects/2026-05-a-share-quant/notes/m4-spike-e-results.md|m4-spike-e-results]]

**指标对比**
| | D（无闸）| **E（+反向闸）** | HS300 |
|---|---|---|---|
| 累计 | -39.45% | **+16.65%** | +40% |
| 年化 | -4.91% | **+1.56%** | +3.47% |
| MDD | -77.90% | **-50.17%** | -45.60% |
| Sharpe | -0.21 | **-0.02** | — |

**第一次跑出正累计收益**。5 行代码改善：累计 +56pp，MDD 降 28pp。

**年度拆分**：9/11 年改善 + 2/11 年恶化
- 大胜年：2016 / 2017 / 2018 / 2022 / 2023（闸门屏蔽单边牛）
- 大败年：**2024 -41.65%**（vs D -2.22%，恶化 39pp）

**2024 事故诊断（关键）**
- 2024-01 单月 **-24.13%** + 2024-08 **-10.23%** = 两次系统性跳水
- 闸门正确识别 HS300 在 SMA60 下方（熊市开仓），但反转策略买"跌幅最大"
- **系统性跳水里"跌幅大"的继续大跌 → 双杀**
- 闸门只屏蔽"单边牛"，**不屏蔽"系统性跳水"**

**新诊断：反转策略两种失效场景**
1. 单边牛市 → Spike E 已解决 ✓
2. 系统性跳水 → Spike E 未解决 ✗，需 ATR 止损或绝对跌幅闸

**数学上为什么跑不过大盘**
- 开仓时间仅 47.37%（闸门关过半）
- 总年化 = 开仓期年化 × 0.47 → 要过验收线年化 20%，开仓期得年化 40%+
- 裸反转信号 α 不够强

**推荐跳过候选 1.7（E + ATR），直接上候选 3（行业两层）**
- 候选 2 残差反转 ~100 行：α 从"±0.45 状态相关"变"稳定 +0.15"
- 候选 3 行业动量 → 行业内反转 ~200 行：α 更强 + 事前分散 + MDD 天然低（聚宽案例 MDD 13%）
- 选候选 3 因为它同时解决 α、分散、MDD 三件事，工程增量可接受

**下一步：候选 3 · 行业两层结构**

## [2026-05-09] M4 Spike F · 行业两层反转 · 首次跑赢 HS300
**决策三问**：
- 行业用 tushare `industry` 字段（110 三级分类，先直接用）
- 行业动量 = 行业内个股 mom_20 等权平均
- 外 M=10 行业 × 内 K=1 股 = 10 仓位（与 E Top10 对照）

**改动**：`prepare_data` 加行业映射 + `industry_mom` 矩阵（~20 行）；`make_spike_f_strategy` ~80 行
- 报告：[[projects/2026-05-a-share-quant/notes/m4-spike-f-results.md|m4-spike-f-results]]

**结果**
| | E（无行业）| **F（行业两层）** | HS300 |
|---|---|---|---|
| 累计 | +16.65% | **+67.70%** | +40% |
| 年化 | +1.56% | **+5.33%** | +3.47% |
| MDD | -50.17% | **-45.44%** | -45.60% |
| Sharpe | -0.02 | **+0.16** | — |
| **超额年化** | -1.91% | **+1.86%** | — |

**首次稳定跑赢大盘**。Sharpe 转正，MDD 与基准持平。

**年度拆分**：
- **大胜年**：2016 (+51.79%) / 2018 (+6.68% vs E -11.29%) / 2024 (-32.42% vs E -41.65%) —— 行业分散效果最明显
- **稍逊年**：2022 / 2023 —— 行业分散分掉了"单一赛道大胜"的 α

**验证行业分散生效**：2016 年 255 笔交易涉及 15+ 行业，单行业最大占比仅 7%

**距验收线（年化 ≥20% / Sharpe ≥0.8 / MDD <35%）仍远**：
- 2024 跳水期仍亏 -32%（行业分散只救了 9pp）
- 开仓时间仅 47%，数学上限制年化
- 手续费 22.8 万占本金 22%

**三条路径**
- A. 继续单变量加 ATR 止损 → Spike G（~50 行）
- B. 直接跳候选 2 残差反转 → Spike H（~100 行）
- C. 停止 Spike 链，正式立项 M4

**我倾向 A 再试一次**：ATR 是通用模块，单变量验证它对 F 的贡献 → 若 MDD 能降到 -30%，直接进 M4 正式版

**下一步：Spike G (F + ATR 止损) 或 C (M4 正式立项)，待用户定**

## [2026-05-09] M4 Spike G · F + ATR 止损 · 反直觉：ATR 杀反转 α
**设计**：ATR_14 × 2.0 止损，每日检查持仓 close vs (entry - 2*ATR_entry)，触发就踢出 last_weights
- 扩 `prepare_data` 加 close/ATR 矩阵
- `make_spike_g_strategy` ~120 行：每日先检查止损 → 再跑 F 选股逻辑
- 报告：[[projects/2026-05-a-share-quant/notes/m4-spike-g-results.md|m4-spike-g-results]]

**结果（反直觉）**
| | F | **G (ATR 2.0)** | 差 |
|---|---|---|---|
| 累计 | +67.70% | **+21.59%** | **-46pp** ✗ |
| 年化 | +5.33% | +1.98% | -3.35pp |
| MDD | -45.44% | -45.10% | -0.34pp（几乎不动）|
| Sharpe | +0.16 | -0.00 | -0.16 |

**最糟糕的止损结果**：代价 -46pp，收益 MDD 只降 0.34pp。

**ATR 倍数扫描（单变量）**
| 倍数 | 累计 | 年化 | MDD |
|---|---|---|---|
| 1.5 | +29.98% | 2.67% | -43.52% |
| 2.0 | +21.59% | 1.98% | -45.10% |
| 2.5 | +34.36% | 3.01% | -43.91% |
| 3.0 | +44.96% | 3.80% | -43.45% |
| 4.0 | +51.89% | 4.29% | -45.24% |
| ∞（F）| +67.70% | 5.33% | -45.44% |

**单调趋势**：越松越好。最优 = "没有止损"。MDD 几乎不随倍数变化 → ATR 无法降反转策略 MDD。

**年度诊断（关键）**
- 救 2024 跳水 **+7pp**（唯一救的年）
- 其余 10 年共计 **-53pp**
- 震荡反转典型年 2021/2023/**2025 (-14.2pp)** 被 ATR 杀得最惨

**根因：反转 vs ATR 的假设矛盾**
- 反转假设：跌的股票会反弹
- ATR 假设：继续跌说明判断错了，砍仓
- 两者方向相反 → ATR 在 V 形底部杀仓，错过反弹

**与 prior-art §3.4 共同模式第 5 条印证**：
> "止损用得少，纯因子策略一般不做。社区实盘把回撤压到 -30% 靠的不是止损，而是事前分散"

**2024 跳水的正确处理是"大盘跳水识别"**（整体空仓），不是"个股 ATR 止损"（杀在 V 底）

**Spike F 可能已是当前框架极限**
四层（闸门 + 月频 + 行业分散 + 反转）再加 ATR 是错误方向。下一个突破要结构性改变。

**下一步三选一**
- A. 认定 F 是极限，正式立项 M4（以 F 为 baseline）
- B. Spike H = F + 残差反转（剥离市场 + 行业 beta，~100 行，预期救单边牛市年）
- C. 换持仓期（mom_n 改 10 或 5，换手会爆炸）

**我倾向 B**：G 明确指向需要结构性改变；残差反转是调研第二重要的改造

## [2026-05-09] M4 Spike H · 残差反转 · 揭示 F 的"运气成分"
**设计**：F 内层信号从原始 mom_20 换成 residual_mom_20（60 日滚动 OLS vs HS300 取残差累加）
- `prepare_data` 加 18 行（滚动 beta + residual_mom 计算）
- `make_spike_h_strategy` ~80 行，只改内层，外层行业动量 + 闸门 + 月频不变
- 报告：[[projects/2026-05-a-share-quant/notes/m4-spike-h-results.md|m4-spike-h-results]]

**结果表面上跑输 F，但剔除 2016 后 H 全面胜出**

| 指标（全样本）| F | H |
|---|---|---|
| 累计 | +67.70% | +32.97% |
| 年化 | +5.33% | +2.90% |
| Sharpe | +0.16 | +0.05 |

| 指标（剔除 2016）| F | **H** |
|---|---|---|
| 累计 | +8.66% | **+24.22%** |
| 年化 | +0.93% | **+2.44%** |
| MDD | -45.44% | **-43.78%** |
| Sharpe | -0.054 | **+0.022** |

**F 的 +67% 几乎全部来自 2016 一年（+51.79%）**——熔断后抄底整体反弹的 β 贡献，不是 α。

**年度诊断完美印证 prior-art**（BigQuant 预测残差 ICIR +0.15）：
- H 救单边牛市年：2019 +7pp、2020 +5.8pp
- H 救熊市：2022 +5.9pp、2018 负贡献
- H 唯一输给 F 的是 **2016 -46pp**（H 正确地认为这是 β 不是 α）

**关键洞察**：F 看起来好是 2016 运气，**不是可复制的 α**。H 是"F 去掉运气后的诚实版"。

**M4 方向校准**
- M4 正式版 baseline 应是 H 不是 F
- F 往下所有优化（G ATR 止损，包括将来可能的其他）都在"跟 2016 运气斗争"，必然反效果
- H 的数字不漂亮但样本外更可复制

**都仍跑输 HS300**（2017-2026 HS300 年化 4.28% vs H 2.44%）→ 反转 α 本身强度不够，需要更多信号叠加

**三条后续路径**
- H1 剥行业 β（~30 行，预期 +1-2pp）
- H2 换手率加权动量（~30 行，剔涨停脉冲，预期 +0.5-1pp）
- **H3 多窗合成反转（~50 行，抓 10 日 IC 0.051 比 20 日 IC 0.038 强 34%）**

**倾向 H3**：抓"更强的信号窗口"而不是"更多去 β"

## [2026-05-09] 引擎 vs 实验 · 边界整理
**触发**：用户问"如果想研究新策略要新开 project 吗、怎么共享引擎"
**对齐**：下一个策略是 A 股另一方向（事件驱动/指数增强/小市值），与本 project 同源 → **引擎共享，各 project 跑自己的 experiments**

**整理动作（步骤 A，未真正迁移引擎）**
- 新建 `deliverables/experiments/{scripts,data}`
- `data-pipeline/scripts/` 只保留引擎通用（bootstrap / daily_update / healthcheck / ingest_benchmarks）
- `data-pipeline/data/` 只保留共享数据（DuckDB + bootstrap.log + healthcheck.json）
- 实验脚本 `hello_world.py` / `m4_spike.py` 搬到 `experiments/scripts/`
- 实验产物 `hello_world*.{csv,json}` / `m4_spike_*.{csv,json}` 搬到 `experiments/data/`

**代码改动**
- 两个实验脚本加 `ENGINE_ROOT = HERE.parent.parent / "data-pipeline"`，自动 sys.path
- 新 `experiments/scripts/__init__.py` 让 `python -m scripts.m4_spike` 可用
- `data-pipeline/README.md` 加"边界"章节
- 新 `experiments/README.md`
- 主 `README.md` 指向两个子目录

**验证**：`cd experiments && ../data-pipeline/.venv/bin/python -m scripts.m4_spike --which F` 跑通，2016 单年 NAV +51.77% 与历史 F 一致

**下一个 project 的共享方式**（未做，留记）
- 新 project `projects/YYYY-MM-xxx/deliverables/experiments/` 自己的实验目录
- 新 project 用 path dependency 指回 `2026-05-a-share-quant/deliverables/data-pipeline`
- DuckDB 文件天然共享（2.2GB 重拉要 3 小时）
- M5 之后若有第二个实盘策略，可考虑把 `data-pipeline/` 升级为 `practices/quant-investing/engine/`

**继续 Spike H3 前这一步是准备性工作**，未改引擎代码本身

## [2026-05-09] M4 Spike H3 · 多窗合成残差反转 · 综合最强
**设计**：H 的内层 residual_mom_20 替换为 **residual_mom_{5,10,20} rank 等权合成**
- 调研：10 日反转 IC 0.051 > 20 日 IC 0.038（强 34%）；5 日为短期反转
- 合成方式：三窗 ascending rank 取平均（避免 raw 加权给短窗 1/4 权重）
- 保留"rm10 < 0"的"确实在跌"过滤
- 报告：[[projects/2026-05-a-share-quant/notes/m4-spike-h3-results.md|m4-spike-h3-results]]

**全样本结果**
| | F | H | **H3** | HS300 |
|---|---|---|---|---|
| 累计 | +67.70% | +32.97% | **+52.83%** | +40% |
| 年化 | +5.33% | +2.90% | **+4.35%** | +3.47% |
| MDD | -45.44% | -43.78% | **-41.10%** | -45.60% |
| Sharpe | +0.16 | +0.05 | **+0.13** | — |
| 超额 | +1.86% | -0.57% | **+0.88%** | — |

**剔除 2016（F 运气年）后（2017-2026 9 年）**
| | F | H | **H3** |
|---|---|---|---|
| 累计 | +12.05% | +24.22% | **+41.67%** |
| 年化 | +1.27% | +2.44% | **+3.95%** |

**H3 样本外最强**：年化比 H 高 1.51pp，比 F 高 2.68pp，MDD 最低。

**年度关键**
- **H3 大胜年**：2021 (+17.4pp vs H) / 2025 (+13.9pp) / 2024 (+5.8pp)
- **H3 大败年**：2018 (-11.3pp) / 2020 (-9pp) / 2017 (-3.8pp)
- 多窗在"行情切换/跳水反弹"大胜，在"单边趋势"小输。净值大胜盖过小输

**2024 跳水终被救 6pp**（H3 -25.92% vs F/H -32%）
多窗 5 日快速信号识别"不是真反转"，无需硬止损

**距验收线仍远**（年化 ≥20% / Sharpe ≥0.8）：MDD 接近（-41% vs -35%），但年化和 Sharpe 差距说明 α 上限在该框架内接近极限

**H3 可作为 M4 v1 baseline**
- 稳定跑赢 HS300（+0.88% 全样本，+2.68pp/年 ex-2016）
- 样本外可复制
- 后续改造（行业残差、换手加权、短窗）边际递减，属 M5 内容

**下一步三选一**
- A. 基于 H3 收尾 M4 正式版（推荐）
- B. 继续 Spike I 单变量（再去行业 β / 换手加权 / skip-1）
- C. 换短窗（mom_n=10 或 5）

**倾向 A**：Spike 链收益递减，H3 已够作 baseline。后续改造属 M5

## [2026-05-09] M4 收尾 · 策略方向不成功，但过程完整 · 经验回流准备
**用户对齐**：本项目策略方向看起来不成功，但作为一次策略尝试，**需要充分总结好经验方法和量化模式**
**收尾动作**：三份正式交付物 + brief 勾选

**交付 1**: [[projects/2026-05-a-share-quant/notes/m4-retrospective.md|m4-retrospective.md]]（本次最重要产出）
- §1 结论先行：H3 是最终 baseline，不达验收但跑赢 HS300
- §2 Spike 链时间线（A→H3 一日 10+ 单变量实验）
- §3 **五个反直觉发现**
  1. 裸动量 ≠ 弱动量，而是反向策略（A 股 ICIR -0.244）
  2. 状态闸门的"方向"是因子属性决定的（C 顺势 -96% vs E 反向 +16%）
  3. ATR 止损在反转策略里反效果（G 扫描验证：越松越好）
  4. 样本外稳定性 > 样本内"最佳"（F 的 +67% 靠 2016 运气）
  5. 多窗"大胜覆盖小输"（H3 年度 6 胜 5 输但净值大胜）
- §4 **七条量化策略开发方法论**（核心回流物）
  1. 调研先行 比 跑 1000 次回测更省时
  2. Spike 链 = 单变量实验 + 归因
  3. 年度拆分 > 全样本指标
  4. 反直觉结果是调研信号
  5. 诚实分层：α / β / 运气
  6. 验收线是"质量门"不是"是否启动"
  7. 工程一次投入，策略一次性
- §5 技术侧教训（5 个真 bug 记录 + 性能拐点 + 数据源坑分级）
- §6 仍未解决的问题
- §7 下一步建议（本次 / 短期 / 中期）
- §8 **候选回流物**（→ wiki，M5 由 project-retro skill 处理）

**交付 2**: [[projects/2026-05-a-share-quant/deliverables/m4-strategy-v1.md|m4-strategy-v1.md]]
- H3 固化规格书（Industry Two-Layer Multi-Window Residual Reversal）
- 参数默认值表 + 核心公式 + 重现命令
- 已知局限 + 扩展方向（参数化预留）

**交付 3**: [[projects/2026-05-a-share-quant/deliverables/m4-report.md|m4-report.md]]
- 按 strategy-selection §六 格式的官方回测报告
- 四项关键指标全不过 + 年度详细 + 归因 + 样本外稳定性

**brief 更新**
- M4 里程碑勾选（正式完成）
- 交付物清单全部勾选（strategy-selection / data-pipeline / backtest / m4-strategy-v1 / m4-report / notes）
- M5 里程碑：启动 project-retro skill

**M5 候选回流物（→ wiki）**
- A 股短期反转 > 动量的实证 → concepts/business/
- 量化策略开发方法论（7 条） → concepts/business/ 或 synthesis/
- Spike 链复盘（A→H3） → synthesis/
- 5 个反直觉发现 → synthesis/
- Tushare / DuckDB 实体页 → entities/products/
- 回测引擎 T+1 / 停牌 / 涨跌停防御清单 → concepts/programming/

**项目状态**：active → 等待触发 M5 project-retro → done（保留目录，wiki/index 摘出活跃表格）
