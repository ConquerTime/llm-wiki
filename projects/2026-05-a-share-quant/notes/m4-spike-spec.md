# M4 Spike · 规格书

> 2026-05-09。两种趋势形态各跑一版最小可行策略，对比后决定 M4 正式版基线。
> 锚点：[[../deliverables/strategy-selection.md|strategy-selection]] §3.3 "M3 首轮 = 纯趋势；M4 叠加 = 弱形式事件过滤"

## 1. 目标

**这不是 M4 正式版**，是决定 M4 基线的试金石。产出：

- 两个 Spike（A 单票 / B 横截面）各跑出一份 10 年回测
- 在相同口径下对比（年化/Sharpe/MDD/Calmar/换手/交易数）
- 决定 M4 正式版用哪种形态
- 暴露工程坑（全市场扫描的速度、数据稀缺性、内存）供 M4 正式版解决

**Spike 不求合格**，即便两个都不过 [[../deliverables/strategy-selection.md]] 六项验收线也没关系。

## 2. 两个 Spike 共同规格

### 2.1 信号：回看窗动量

过去 N 日涨幅：`mom_N = close[t] / close[t-N] - 1`

简单起见，首版用 **单窗 20 日动量**。N=20 在 A 股是最常用的月动量口径。
后续可以加权合成（20/60/120），作为迭代点。

### 2.2 样本池（负过滤，仅用现有数据）

每日收盘后，按以下规则**过滤掉**不合格标的：

| 过滤规则 | 数据来源 | 阈值 |
|---------|---------|------|
| ST / *ST 股 | stock_basic.name | name 含 "ST" |
| 已退市 | stock_basic.list_status | != 'L' |
| 北交所（.BJ） | ts_code 后缀 | 排除 |
| 上市不足 250 个交易日 | stock_basic.list_date | list_date + 250 trade_days > asof |
| 当日无成交（停牌） | daily_bar 当日有无记录 | 缺记录即剔 |
| 当日成交金额末 20% | daily_bar.amount 全市场排序 | 当日后 20% 剔 |
| M2 体检 11 只 active 无日线 | 硬编码剔除列表（已修复，但保留为安全网）| — |

*不做*：财务质量过滤（fina_indicator 覆盖稀疏，会误杀大量样本）
*不做*：涨跌停当日买入限制（简化）—— 实盘执行层做

### 2.3 回测期 & 基准

- 样本期：**2016-01-01 ~ 2026-05-08**（必覆盖 2018 熊市、2021 风格切换、2024.1 跳水）
- 初始资金：100 万
- 基准：000300.SH 沪深 300 指数（跨标用法，Bug 2 修复后已支持）
- 手续费：沿用引擎默认（买 0.025%，卖 0.125%）
- 滑点：不模拟（Spike 阶段简化）
- 涨跌停拒单：不模拟

### 2.4 评价口径

按 [[../deliverables/strategy-selection.md]] §六的六项 + 换手。不看合格线，只看**数值差异**和**曲线形态**。

## 3. Spike A · 单票时序动量

**假设**：每日找全市场动量最强的那只股票，满仓持有一天。

**决策流程**：
```
每日收盘 t:
    pool = negative_filter(asof=t)
    top1 = pool.loc[pool["mom_20"].idxmax(), "ts_code"]
    return {top1: 1.0}
次日开盘：卖出昨日持仓，买入 top1（受 T+1 影响，昨日买入的不能今日卖）
```

**已知风险**：
- **换手极高**：若每日 Top1 都不同，年换手 200 倍以上
- **T+1 失效**：今日开盘把昨日买入的换成今日新 Top1 → 被 T+1 拦截
- 预期：交易数极多、手续费吞噬收益、Sharpe 可能很差

**引擎现实约束**：
- 引擎当前 T+1 语义 = 信号当日收盘，下一开盘成交。但**它不会拒绝"卖昨日刚买的"**。Spike 阶段接受这个不合规，产出结论时明确披露
- M4 正式版若选 A，必须加"持有 ≥1 个交易日才能卖"约束

## 4. Spike B · 横截面 Top-K 动量

**假设**：每日选全市场动量前 K 名，等权持有。K=10 起步。

**决策流程**：
```
每日收盘 t:
    pool = negative_filter(asof=t)
    top_k = pool.nlargest(10, "mom_20")["ts_code"]
    return {code: 0.1 for code in top_k}  # 等权 10%
```

**已知风险**：
- 每日全换仓依然换手极高
- **改良**：每 M 个交易日换仓一次（月频 M=20 / 周频 M=5），显著降换手
- 首版 Spike：**固定月频换仓（M=20）**，跟动量策略研究惯例

## 5. 工程实现路线（按简单优先）

**不改引擎**，三件事：

1. 新增 `quant_data/universe/filters.py`：每日返回合规股票 list[str]（~80 行）
2. 新增 `quant_data/factors/momentum.py`：计算 mom_N（~30 行）
3. 新增 `scripts/m4_spike.py`：协调器，分别跑 A 和 B，写报告

**预期性能风险**：
- B 策略要求每日访问全市场 bars。若把 5800 只 bars 全部 load 进内存（~1GB），单次回测 2500 日 ≈ 几分钟。可以接受
- A 策略同理

如果跑太慢（> 30 分钟单次），降级为：Top1 改 Top5-20 名里随机选 / 横截面 K 改 20 / 采样部分股票

## 6. 产出清单

- [ ] `notes/m4-spike-spec.md`（本文档）
- [ ] `quant_data/universe/filters.py`
- [ ] `quant_data/factors/momentum.py`
- [ ] `scripts/m4_spike.py`
- [ ] `notes/m4-spike-results.md`（对比表 + 曲线图 + 选型结论）
- [ ] `data/m4_spike_A.csv/json` + `data/m4_spike_B.csv/json`
- [ ] `notes/m4-spike-nav.png`（三线：A / B / HS300）
- [ ] log 追加

## 7. 选型决策树

跑完 Spike 后，按以下流程决定 M4 正式版：

```
if A 或 B 任一 Sharpe >= 0.6 且 MDD < 50%:
    选赢家进 M4 正式版
    M4 迭代项：信号（20/60/120 多窗）+ 事件过滤器完善 + 换手控制
else if A 和 B 都远不合格:
    M4 正式版直接改做 备选方向"小市值多因子（进攻版）"
    strategy-selection §4 已有骨架
else if 两者都在及格边缘:
    合并：横截面 Top-K + 单票动量过滤
    工程量高，慎选
```

## 8. 开放问题（Spike 跑完后回答）

- 5800 股 × 2500 日的全市场扫描实际速度是多少？（决定 M4 是否需要预计算 factor 表）
- 20 日动量是不是足够分辨信号？60/120 是否必要？
- 负过滤"成交金额末 20%"是否误杀过多？
- Spike 期间交易数 / 手续费占比（如果 >30% 吞噬），M4 必须换成月频
