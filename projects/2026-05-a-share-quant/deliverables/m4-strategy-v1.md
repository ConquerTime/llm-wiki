---
project: 2026-05-a-share-quant
status: active
created: 2026-05-09
updated: 2026-05-09
---

# M4 Strategy v1 · 规格书（Spike H3 固化）

> 2026-05-09。M4 交付物。基于 Spike H3 的可重现策略定义 + 参数默认值 + 重现命令。

## 1. 名字与定位

**Strategy v1 · Industry Two-Layer Multi-Window Residual Reversal**

简称 **M4-v1** 或 **H3-frozen**。

**定位**：
- A 股横截面**短期反转**策略
- 月频调仓，小仓位分散
- **跑赢 HS300 基准**但**不达 brief §六验收线**
- 作为后续策略迭代的 baseline，不作为实盘候选

## 2. 核心公式

```
每日收盘后 t:
  # 1. 大盘状态闸门（反向：牛市空仓）
  if HS300.close[t] > HS300.close.rolling(60).mean()[t]:
    target_weights = {}  # 空仓
    return

  # 2. 月频换仓判定（距上次换仓 < 20 交易日则维持）
  if days_since_last_rebalance < 20:
    return last_weights

  # 3. 外层：选"行业 20 日动量"跌最多的 Top 10 个行业
  industry_mom[ind, t] = mean(stock_mom_20[s, t] for s in ind)  # 行业内股票 mom_20 等权
  selected_industries = industry_mom.nsmallest(10)[industry_mom < 0]

  # 4. 内层：多窗残差动量 rank 等权合成
  # 残差动量 = 剥离市场 β 后的累计收益
  beta_i = cov(r_i, r_HS300, 60) / var(r_HS300, 60)
  residual_i = r_i - beta_i * r_HS300
  residual_mom_N[i, t] = sum(residual_i[t-N+1 : t])  for N in {5, 10, 20}

  # 三窗 rank 等权合成
  combined_rank[i, t] = mean(rank_asc(residual_mom_N[:, t])  for N in {5, 10, 20})

  # 5. 每个选中行业内按 combined_rank 升序选 Top 1
  #    且用 residual_mom_10 < 0 过滤（确认"真在跌"）
  for each ind in selected_industries:
    candidates = stocks in ind with rank(combined, asc) 低 AND residual_mom_10 < 0
    pick = nsmallest(1, combined_rank)

  # 6. 等权分配：持仓 = 10 只等权
```

## 3. 参数默认值

| 参数 | 值 | 说明 |
|---|---|---|
| `mom_n` | 20 | 行业动量窗口（外层）|
| `top_industries` (M) | 10 | 外层选几个行业 |
| `top_per_industry` (K) | 1 | 内层每个行业选几只 → 共 10 仓 |
| `rebalance_interval` | 20 | 月频换仓（单位：交易日）|
| `residual_windows` | [5, 10, 20] | 多窗残差动量 |
| `residual_beta_window` | 60 | 滚动 OLS 回归窗口 |
| `regime_gate` | `HS300 > SMA60 → 空仓` | 反向闸门 |
| `initial_cash` | 1,000,000 | 初始资金 100 万 |
| `buy_fee` / `sell_fee` | 0.025% / 0.125% | A 股常规（含印花税）|

## 4. 样本池规则

按 [[../notes/m4-spike-spec|m4-spike-spec]] §2.2 的 7 条负过滤：

| 过滤 | 阈值 / 规则 |
|---|---|
| ST / *ST | name 含 "ST" |
| 已退市 | list_status ≠ 'L' |
| 北交所 | ts_code 后缀 ≠ '.BJ' |
| 次新股 | 上市日历日 ≥ 250 天 |
| 当日停牌 | daily_bar 无记录 |
| 流动性末 20% | 按日 amount 截面 |
| 硬编码黑名单 | M2 体检的 11 只（已修复，保留为安全网）|

## 5. 重现命令

```bash
cd projects/2026-05-a-share-quant/deliverables/experiments

# 跑 H3，输出到 data/m4_spike_H3.{csv,json}
../data-pipeline/.venv/bin/python -m scripts.m4_spike --which H3

# 完整参数扫描（A-H3 全链 + ATR sweep）
../data-pipeline/.venv/bin/python -m scripts.m4_spike --which H3 \
  --mom-n 20 --top-industries 10 --top-per-industry 1 --rebalance 20
```

**回测产出**：
- `data/m4_spike_H3.json` — 参数 + 指标 + 交易数
- `data/m4_spike_H3.csv` — 每日 NAV + 基准 NAV

## 6. 核心代码入口

| 文件 | 函数 | 行数 |
|---|---|---|
| `experiments/scripts/m4_spike.py` | `make_spike_h3_strategy` | ~100 |
| `data-pipeline/quant_data/backtest/engine.py` | `BacktestEngine.run` | ~250 |
| `data-pipeline/quant_data/universe/filters.py` | `negative_filter_asof` | ~80 |
| `data-pipeline/quant_data/api.py` | `get_bars`（前复权 qfq）| ~120 |

## 7. 已知局限

1. **未实现涨跌停拒单**：引擎不模拟涨停无法买入 / 跌停无法卖出。实盘前必须补
2. **未实现滑点**：按 open 原价成交。实盘前加 5-10 bp 冲击成本
3. **财务过滤未用**：fina_indicator 覆盖稀疏（M2 体检发现），本策略不依赖
4. **ATR 止损未启用**：Spike G 证明会杀 α，当前默认关闭

## 8. 扩展方向（参数化预留）

M4 v1 **刻意不实现**以下选项，留给 v2+：
- `--use-atr-stop` / `--atr-mult`：可选 ATR 止损（Spike G 验证已失败，保留接口）
- `--single-window`：退回单窗 20（H 的形态）
- `--no-regime-gate`：关闭大盘闸门（D 的形态）
- `--gate-direction`：顺势/反向（C 的形态）
- `--residual-type`：market_only / market_industry / none

参数化实现留给 M5 或第二个策略 project。

## 9. 相关文档

- [[../notes/m4-spike-h3-results|Spike H3 详细结果]]
- [[../notes/m4-retrospective|M4 复盘与方法论]]
- [[../notes/m4-prior-art|Prior-art 调研]]
- [[strategy-selection|M1 策略选型]]
