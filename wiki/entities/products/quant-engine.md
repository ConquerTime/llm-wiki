---
title: quant-engine
type: entity
subtype: product
tags: [tool, business]
created: 2026-05-09
updated: 2026-05-09
sources:
  - "[[projects/2026-05-a-share-quant/retro.md|2026-05 a-share-quant 项目复盘]]"
  - "[[projects/2026-05-a-share-quant/deliverables/m4-strategy-v1.md|M4 Strategy v1 规格]]"
---

# quant-engine

> a-share-quant 项目自研的 A 股量化回测引擎，~350 行 Python，以 `strategy(asof, bars, portfolio) -> weights` 协议为核心。计划在多个 A 股策略 project 之间共享。

## 一句话介绍

**一个"五字协议"就用完的轻量回测引擎** —— 策略函数返回目标权重字典，引擎负责 T+1 / 停牌 / 手续费 / NAV 核算。

## 基本事实

- **位置**：`practices/quant-investing/engine/quant_data/backtest/`（2026-05-09 从 `projects/2026-05-a-share-quant/deliverables/data-pipeline/` 迁入以实现跨 project 共享）
- **代码量**：`engine.py` ~250 行 + `metrics.py` ~120 行
- **Python**：3.11+，uv 管理
- **依赖**：pandas / numpy / duckdb / tushare / matplotlib
- **License**：项目内部（未开源）
- **诞生**：[[projects/2026-05-a-share-quant/notes/m3-decisions.md|M3 决策]] 评估 qlib/Backtrader/rqalpha 后选自研
- **验证**：[[projects/2026-05-a-share-quant/retro.md|M4 Spike 链]] 跑 10+ 个单变量实验均通过

## 核心协议

每日收盘后调用策略函数，返回目标权重：

```python
def strategy(
    asof: pd.Timestamp,             # 当日日期
    bars: dict[str, pd.DataFrame],  # 所有 bars（或切片）
    portfolio: Portfolio,           # 当前持仓 + 现金
) -> dict[str, float]:              # {ts_code: weight ∈ [0, 1]}
    ...
```

引擎把目标权重**在次日开盘**执行（T+1 合规），计算手续费 + 更新持仓 + mark-to-market。

**为什么这个协议好用**：
- 策略函数**无副作用**（纯读数据 + 返回 dict）
- 可测试、可对比、可组合
- [[projects/2026-05-a-share-quant/notes/m4-retrospective.md|M4 Spike 链]] 10+ 策略都用同一协议，每个只 30-150 行

## 关键模块

| 模块 | 职责 |
|---|---|
| `backtest/engine.py` | 主循环：T+1 执行、持仓记账、手续费、停牌冻结 |
| `backtest/metrics.py` | 年化 / Sharpe / MDD / Calmar / 换手 / buy_and_hold_nav |
| `universe/filters.py` | 样本池负过滤（ST / 停牌 / 次新 / 流动性 / 北交所）|
| `factors/momentum.py` | 动量因子（Spike 用；策略可自写其他因子）|
| `api.py` | 统一读数：get_bars / get_stock_list / get_trading_dates / get_fina_indicator |
| `storage/duckdb_store.py` | DuckDB schema + 幂等 upsert + 进度表 |

## 关键设计

### 内建 [[backtest-engine-defense-checklist|四条防御]]

引擎层一次性内建：
- **T+1 语义**：信号 t 收盘算，成交 t+1 open
- **停牌断点**：当日无 bar → 持仓冻结，NAV 用上一 close
- **复权跳变**：启动扫描 suspect_days（|ret|>30%），不中断
- **前瞻偏差**：`get_fina_indicator(as_of_date=...)` 用 ann_date 过滤

策略层不需再重复实现。

### fast_mode 开关

单标的策略：`bars_hist = {code: df.loc[:asof]}` 切片传入
全市场策略：`fast_mode=True`，直接传 bars reference，策略自 asof 对齐
- 性能差 50×（5800 股 × 2500 日的切片开销）
- 对 M4 全市场 Spike 至关重要

### 手续费模型

- 买入 0.025%（佣金）
- 卖出 0.125%（佣金 + 印花税）
- 无滑点（Spike 阶段简化，实盘前要加 5-10 bp）

### DuckDB 存储

单文件 2.2 GB 存全市场 10 年 × 7 张表（daily_bar / adj_factor / daily_basic / fina_indicator / stock_basic / trade_cal / ingest_progress）。单机 SQL 秒级全市场查询。见 [[duckdb]] 实体页。

## 已验证的局限

本引擎**不实现**：

- 涨跌停拒单（Spike 简化）
- 日内回转 / 高频
- 保证金 / 融资融券
- 期货 / 期权
- ML 训练框架（与 qlib 的核心差异）

实盘前必须补的：
- 涨跌停拒单（当日 open 已触涨停 → 跳过不补位）
- 滑点模型（5-10 bp 冲击成本）

## 设计权衡 vs qlib / rqalpha

[[projects/2026-05-a-share-quant/notes/m4-prior-art.md|prior-art 调研]] 已详细评估：

| 方案 | 为什么不选 |
|---|---|
| qlib | ML 训练框架不是策略引擎；绑 binary 私有格式；策略代码不能迁移到轻量协议 |
| Backtrader | 2023 停维护；A 股适配层仍要自写 |
| rqalpha | 官方 examples 全 CTA 择时，无横截面；绑米筐数据 |
| zipline-cn | 停更 2+ 年 |
| 自研（本项目）| 350 行覆盖本 project 全部需求；Spike 链每次改 30-150 行即可 |

**结论**：开源生态里没有"原生支持横截面选股 + 自定义 asof 协议"的引擎。自研成本 < 迁移成本。

## 跨 project 共享

2026-05-09 起的边界：
- 引擎（本实体）= `practices/quant-investing/engine/` —— 跟 practice 生命周期，不随 project 归档消失
- 实验（特定策略的 Spike 脚本 + 产出数据）= 各 project 的 `deliverables/experiments/`

下一个 A 股策略 project 启动时，其 experiments 脚本顶端添加：
```python
VAULT_ROOT = Path(__file__).resolve().parents[4]  # 上溯到 vault
ENGINE_ROOT = VAULT_ROOT / "practices" / "quant-investing" / "engine"
sys.path.insert(0, str(ENGINE_ROOT))
```

DuckDB 文件天然共享（2.2 GB 重拉成本 3 小时）。

## 相关条目

- [[backtest-engine-defense-checklist|回测引擎防御清单]] — 本引擎内建的四条防御规范
- [[quant-strategy-spike-methodology|量化策略 Spike 开发方法论]] — 本引擎设计的"为什么"，以及 Spike 链如何用它
- [[tushare-pro|Tushare Pro]] — 本引擎的主数据源
- [[duckdb|DuckDB]] — 本引擎的存储层
