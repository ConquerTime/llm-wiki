---
title: 回测引擎防御清单
type: concept
subtype: quant-infra
tags: [programming, business]
created: 2026-05-09
updated: 2026-05-09
sources:
  - "[[projects/2026-05-a-share-quant/retro.md|2026-05 a-share-quant 项目复盘]]"
  - "[[projects/2026-05-a-share-quant/notes/m2-data-healthcheck.md|M2 数据体检]]"
---

# 回测引擎防御清单

> 量化回测的"正确"不是跑出漂亮曲线，而是跑出**可信**曲线。四条底层防御（T+1 / 停牌断点 / 复权跳变 / 前瞻偏差）不建在引擎层，就会在策略层的每次改动里悄悄失效。

## 为什么需要这份清单

回测里最常见的**静默作弊**：

- 把**明天的信息**用到今天（前瞻偏差）—— 跑出年化 100% 的 SMA 策略
- 在**股票停牌日**也算净值曲线 —— NAV 线条漂亮，实盘一开始就崩
- 复权价跳变导致**某一日 +200%** 的虚假涨幅 —— 策略吃到不存在的收益
- 允许当日买入当日卖出（T+0）—— 对 A 股基本违规

这些坑**每一条都能让回测收益虚高 5-20 pp**。靠策略层兜底（"我写策略时记得不犯"）不现实：每个新 Spike 都要重写这套保护。**必须放在引擎层一次性内建**，策略层就能干净写规则。

## 四条核心防御

### 1. T+1 成交语义（A 股强制）

**规则**：信号在 t 收盘后生成，成交在 **t+1 的 open**。

**为什么**：
- 信号用当日收盘价计算 + 当日收盘价成交 = **隐含的未来函数**（收盘那一刻你不可能还在市场里交易）
- A 股 T+1 制度：买入当日不能卖出，必须隔夜

**实现骨架**：
```python
for t in dates:
    if pending_weights is not None:
        execute(t.open, pending_weights)   # 昨天信号今天开盘执行
    mark_to_market(t.close)
    pending_weights = strategy(t, ...)     # 今天收盘后才算
```

**踩坑**：持仓换仓时 "昨天买入的当天想再卖"—— 要么引擎显式禁止（严格 T+1），要么在报告里明示"本引擎允许同标的次日开盘调仓"（宽松 T+1）。**必须讲明白**

### 2. 停牌断点识别

**规则**：当日缺 bar = 停牌。引擎**冻结持仓**（不成交 / 不估值跳变），NAV 用上一日 close 续算。

**为什么**：
- 停牌期股票不能交易，强制成交会产生虚假收益
- 停牌前后的价格跳变（如复牌补跌）不能算作策略"损失"，是市场行为
- 检测方式：daily_bar 当日无记录 **或** vol = 0

**实现要点**：
```python
# 每日收盘估值
for code in portfolio.holdings:
    if t in bars[code]:
        portfolio.last_close[code] = bars[code].at[t, 'close']
    # 停牌日不更新 last_close，沿用前值
```

### 3. 复权跳变告警（不 NaN，标记）

**规则**：日收益 |ret| > 30% 的记录**标为 `adj_suspect`**（不是 NaN 不是丢弃），策略层决定是否跳过。

**为什么**：
- 前复权 / 后复权算法有 bug 时会产生单日 > 100% 的虚假涨幅
- 某些数据源（如北交所 adj_factor）初始值异常
- 策略层如果静默接受 = 吃到虚假收益
- 直接丢弃 = 可能丢掉真实的极端事件（涨跌停 + 除权组合）

**实现要点**：
```python
# 引擎启动时扫一遍
ret = bars.close.pct_change()
suspect_days = bars[ret.abs() > 0.30]
log.warning(f"{len(suspect_days)} 日复权跳变，记入 suspect_days，策略自决")
```

### 4. 前瞻偏差防护（ann_date 而非 end_date）

**规则**：财务数据必须用 **ann_date（公告日）** 做 as-of 过滤，不是 **end_date（报告期）**。

**为什么**：
- 2024 Q4 财报的 end_date = 2024-12-31
- 但实际 ann_date 通常是 2025-03 ~ 2025-04（次年一季度）
- 用 end_date 过滤 = 1 月就知道 3 月才公告的数据 = **前瞻偏差 2-3 个月**
- 历史上最经典的"伪阿尔法"之一

**实现要点**：
```python
def get_fina_indicator(ts_code, as_of_date):
    # WRONG: WHERE end_date <= as_of_date
    # RIGHT:
    return query("SELECT * FROM fina_indicator "
                 "WHERE ts_code = ? AND ann_date <= ?",
                 [ts_code, as_of_date])
```

## 样本池层也要守的规则（工程层补充）

不属于回测引擎，但搭一套因子策略前**必须**补：

| 规则 | 阈值 |
|---|---|
| 剔除 ST / *ST | name 含 "ST" |
| 剔除退市 / 特停 | list_status = 'L' |
| 次新股硬过滤 | 上市 ≤ 180-250 日历日 |
| 流动性底部剔除 | 日成交金额末 20% |
| 涨跌停日不买入 | 当日 open/close 已触涨停 → 跳过**不补位** |

**"不补位"很重要**：如果 Top1 涨停买不到 → 不要改买 Top11。这会引入隐性的二阶选择偏差（涨停的 Top1 是强势，Top11 是弱势，变成"被迫买弱势"）。

## 实战验收

每次搭新回测框架 / 改引擎后，跑一遍"**故意作弊测试**"验证防御是否生效：

1. **T+1 测试**：构造一个"当日收盘信号 + 当日收盘成交"的对比，应该跑不出
2. **停牌测试**：找一只长期停牌股，引擎 NAV 不应跳变
3. **复权测试**：找一只北交所或高除权股，检查 suspect_days 计数
4. **前瞻测试**：把 ann_date 换成 end_date 跑一遍，看累计收益差多少（应该差几个 pp）

## 适用范围

- **股票类规则策略**：✓ 全适用
- **期货 / CTA**：T+1 不适用（期货 T+0），其他仍适用
- **ML 模型**：前瞻偏差防护在**特征工程**阶段尤其重要（训练集泄漏 > 回测泄漏）
- **事件驱动**：公告数据的前瞻偏差（用 ann_date）特别容易踩

## 相关页面

- [[quant-strategy-spike-methodology|量化策略 Spike 开发方法论]] — Spike 链开发方法
- [[quant-engine|quant-engine]] — 本清单的一个参考实现（见该实体的"关键设计"章节）
