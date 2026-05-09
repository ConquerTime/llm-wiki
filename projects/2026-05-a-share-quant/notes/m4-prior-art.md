# M4 Prior-Art · 调研报告

> 2026-05-09。在启动 M4 正式版前，调研学术 / 开源 / 社区三个方向。
> 三份 Agent 调研结果合并。结论**颠覆 Spike 阶段的 M4 方向**。

## 0. TL;DR（读这一段就够）

**A 股 ≤1 个月截面是反转因子在主导，不是动量**。

我 Spike B 的"买过去 20 日涨幅最大的 Top 10" = **做反向反转** = 数学期望上必亏。

Spike C（加大盘趋势闸）那 3 个百分点的改善几乎可以视为"随机收敛 + 暴露时间减半"，**不能靠过滤规则把这个策略翻正**。

**M4 正式版必须重选方向**，候选四条见 §5。Spike 阶段原定的"4 个 P0 改造 Spike B"作废。

---

## 1. 学术视角

### 1.1 关键参考

**[1] 白颢睿 / 吴辉航 / 柯岩（清华五道口）《财经研究》2020**
- 2000–2016 全 A 月频动量因子**不显著**
- 归因：T+1 制度下，前期赢家在隔夜存在系统性"折价"，日内动量被隔夜反转抵消，**月频合并后净效应归零**
- 附加解释：彩票型偏好 + 处置效应 → 强势股被打成反转标的

**[2] BigQuant 2015–2025 全 A 动量分层回测**
- 5,487 只股票（含 324 只退市，处理幸存者偏差）
- 回看 3M / skip=0 / 持有 1M 最优参数下：
  - **IC = -0.032**（负！）
  - **ICIR = -0.244**
  - **t = -2.66**
  - G1（低动量）年化 **+9.43%**
  - G5（高动量）年化 **+2.04%**
  - 多空组合 **-6.80%/年**
- 剥离市场 + 行业因子做 **12 月 OLS 残差动量**后：ICIR 由 -0.244 翻为 **+0.15**
- **震荡市 ICIR +0.45，牛市 -0.36**：牛市是反转最烈时

**[3] Zhihu 反转因子实测**（zhuanlan.zhihu.com/p/386661895）
- 10 日反转 **IC = 0.051**、**IR = 0.58**、胜率 **61%**（小市值最强）
- 20 日衰减到 0.038；60 日几乎归零
- 行业动量另一体系：3 月行业动量 IC = 0.042，个股动量 IC 仅 0.01–0.015
- 散户占 ~70% 交易量是根因

**[4] 华泰金工《单因子测试之动量类因子》**
- 测试 13 种动量因子，表现最佳：**exp_wgt_return_6m** 和 **exp_wgt_return_3m**
- 即**"换手率加权"的中期动量**（换手高的日子权重更低）
- 变相剔除"涨停脉冲 / 妖股拉升"的污染

**[5] 次新股处理（量化社区共识）**
- 通行做法：上市**≤180 交易日**（6–9 月）硬过滤
- 次新股期内收益高度不对称（平均跌 14.7% vs 长端涨 5.5%）
- 我的"250 日"标准不够

### 1.2 我 3 条诊断的对照表

| 我的诊断 | 学术验证 | 修正 |
|---|---|---|
| 反转效应 > 动量 | **完整验证** | 更精细：**≤20 日 = 反转主导，3–12 月 = 残差/行业动量主导**。按时间尺度分治 |
| 次新股污染 | 部分验证 | 通行硬过滤**≤180 交易日**；再往后用**换手率加权**软处理 |
| T+1 + 月频迟钝 | **精确验证**（白颢睿）| 不是"迟钝"，是"**日内动量 vs 隔夜反转相互抵消**"。月频正好取到净零区 |

**被调研修正的新增问题**：我 Spike 用的是"**等权 20 日价格动量**"，学术上等价于"吃反转"。即使换窗口，裸价格动量在牛市有 40%+ 概率持续负 IC。

### 1.3 不确定性披露

华泰 exp_wgt_return_3m/6m 的具体 IC 数值、发布日期未查到。中信/海通相关深度研报未找到——这块"来源未查到"。

---

## 2. 开源实现

### 2.1 qlib Alpha158（最直接可抄）

`qlib/contrib/data/loader.py` 的 `Alpha158DL.get_feature_config()`：

```python
# 默认窗口 [5, 10, 20, 30, 60]，所有因子都用 /$close 归一化
ROC    "Ref($close, %d)/$close"        # 过去第 d 日价/今日价（反转型）
MA     "Mean($close, %d)/$close"       # 均线偏离
STD    "Std($close, %d)/$close"        # 波动率
MAX    "Max($high, %d)/$close"         # 区间高点
IMAX   "IdxMax($high, %d)/%d"          # 距最高点天数（反转信号）
CNTP   "Mean($close>Ref($close,1), %d)" # 上涨天数占比
WVMA   "Std(Abs($close/Ref($close,1)-1)*$volume, %d)/(Mean(...)+1e-12)"  # 量价共振
```

**关键**：qlib 的 ROC 方向是 "**过去价/今价**"，**小值看多**（反转方向）。这与我 Spike B 的"今价涨幅排序取大"是**相反方向**。

### 2.2 qlib 的 A 股过滤逻辑（可直接抄）

`qlib/backtest/exchange.py`：

```python
# 涨停判断：pct_chg >= limit_threshold（默认 0.1；创业板/科创板 0.2 通过 tuple）
check_stock_limit(): self.quote_df["$change"].ge(limit_threshold)

# 停牌判断：close 为 NaN
check_stock_suspended(): $close is NaN

# 组合检查
is_stock_tradable(stock_id, start_time, end_time, direction)
```

`qlib/contrib/strategy/signal_strategy.py` 的 `TopkDropoutStrategy`：
- 涨停/停牌**直接跳过，不补位**
- 这很重要 —— "买不到 Top1 就买 Top11" 会引入二阶偏差

### 2.3 WorldQuant 101 Alphas（A 股反转适配）

- **Alpha#4** = `-1 * ts_rank(rank(low), 9)` — 9 日内低点排名，短周期反转
- **Alpha#9** = 条件反转（连涨/连跌延续，否则反转）— 印证"当日 vs 中期"分离思路
- **Alpha#12** = `sign(delta(volume, 1)) * (-1 * delta(close, 1))` — 量变方向 × 价反转
- **Alpha#53** = KDJ 风格反转

### 2.4 其他框架速判

| 框架 | 状态 | 有无价值 |
|---|---|---|
| rqalpha（米筐）| 活跃 | T+1 / ST 逻辑在 `api_stock.py`，但依赖专有数据 |
| zipline-cn | 停更 2+ 年 | 不推荐 |
| **hugo2046/QuantsPlaybook** | 活跃 | **100+ 中信/华泰研报复现，含 RSRS、波动率止损** |
| phonegapX/alphasickle | 活跃 | CSI300 多因子增强 |

### 2.5 结论

从 qlib 抄三件事：
- (a) `is_stock_tradable` 三段式过滤（suspended / limit / direction）
- (b) Alpha158 的 `/$close` 归一化约定
- (c) Top-K + "不补位" 的调仓规则

ATR 止损、次新过滤自己写，**别拖 qlib 依赖**。可参考 `hugo2046/QuantsPlaybook` 的波动率止损代码。

---

## 3. 社区实战

### 3.1 案例 1 · 申万宏源《多周期动量与反转因子研究》
- 新浪财经转载 [rptid=768550409293](https://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/lastest/rptid/768550409293/index.phtml)
- 规则：HS300/CSI500/CSI800/CSI1000 全池以及**30 个行业内截面**，月频调仓分 10 组多空；剔 ST、停牌、上市不足一年
- 回测：样本 2010+（>10 年）；**中证 800 Rank IC = 0.039**（正号，因构建为"反转分组"）
- **行业内最强年化 28.76% / 33.12%**，Sharpe 2.146 / 1.814
- **关键**：多空组合才到 Sharpe 2.0，**纯多头低很多**

### 3.2 案例 2 · Zhihu 反转因子
- [zhuanlan.zhihu.com/p/386661895](https://zhuanlan.zhihu.com/p/386661895)
- 规则：信号 = **过去 1 个月收益率取负**（跌得多的买）；10 分组多空；"结构化反转"引入流动性/波动率剔除噪声
- 回测：月度 **IC = 0.033，年化 ICIR = 2.65**
- lookback 拉到 240 日后 ICIR 退化到 -0.28 → **反转只在 ≤1 月稳定**

### 3.3 案例 3 · JoinQuant《修改行宽-偷鸡》
- [聚宽社区](https://www.joinquant.com/view/community/detail/9eafe20d40f7ad1fb52669370e1f9942)
- 规则：**行业相对 20 日均线强度**做行业动量 → 选 Top 行业 → 行业内选小市值个股；周频；≤5 只持仓
- 回测：年化 **99.59%**，MDD **13.47%**
- MDD 压到 13% 的关键：**"行业动量外层 + 行业内选股内层" 两层结构** + **单仓 ≤20% 事前分散**

### 3.4 共同模式（5 条）

1. **行业/市值中性是底线**：三家都不敢在全市场按涨幅直接排序
2. **A 股短周期 = 反转不是动量**：1 月以内 IC 负，要嘛取反号，要嘛 lookback 拉到 6–12 月并 **skip 最近 1 月**（skip-1-month momentum）
3. **预过滤固定五件套**：涨停次日开盘、ST、停牌、次新、流动性末尾 20%
4. **单票 ≤10% + 行业 ≤30% 事前分散**比止损更有效
5. **止损用得少**，纯因子策略靠**换仓频率控制**而非硬止损

---

## 4. 对 Spike 结果的再诊断

Spike A/B/C 的 -99% 不只是"裸动量失败"，而是**方向错了**。

按 BigQuant 的 IC = -0.032 / ICIR = -0.244：
- 用 mom_20 排序"做多 Top 10" = 在一个 **ICIR 负 0.244** 的信号上**做多**
- 10 年复合 ≈ 理论年化 -8% × 10 = 复利约 -57%（我们跑 -99%）
- 差距的 40+pp 来自：换手手续费 + 次新股极端样本 + 月频迟钝 + 无止损

**关键**：信号**取反号**（买 20 日跌幅最大的）就能把 ICIR 由 -0.244 翻为 +0.244，**不需要任何其他改造**就有约等价的正收益潜力。

---

## 5. M4 方向重选 · 四个候选

原计划"Spike B + 4 P0 改造"**作废**，重选。四个候选按期望 IR 高到低：

### 候选 1 · 反转版 Top-K（最简单，ICIR 估计 +0.5 量级）
- 规则：Spike B 信号**取反**，买过去 20 日跌幅最大的 Top 10
- 加 5 项预过滤（涨停次日、ST、停牌、次新 180 日、流动性末 20%）
- 预估改造成本：~30 行代码（Spike B 加 `nlargest` → `nsmallest`）
- **这是最符合学术共识的最小改造**

### 候选 2 · 残差动量（中期 3-6 月）
- 做 12 月 OLS 残差动量（剥离市场 beta + 行业 beta）
- 月频持有，skip 最近 1 月
- 预期 ICIR +0.15（BigQuant 数据）
- 改造成本：~100 行（需要行业分类数据 + OLS 实现）

### 候选 3 · 行业动量 + 行业内小市值（聚宽案例）
- 先算每个申万行业的 20 日相对强度 → 选 Top 行业
- 行业内选小市值 + 分散持仓（行业 ≤30%）
- 预期：MDD 压到 -30% 以内的可能性最大
- 改造成本：~200 行（需要申万行业分类数据，tushare 有）

### 候选 4 · 多因子合成（反转 + 换手率加权动量 + 波动率）
- 华泰 exp_wgt_return + Zhihu 结构化反转 + 流动性过滤
- 预期表现最好，但工程量最大
- 改造成本：~400 行

### 推荐（按"最小验证"优先）

**候选 1 → 候选 3**：
- 先做**候选 1**（30 分钟能跑出数字），验证"反号 = 正收益"
- 如果候选 1 年化 > 10%，推进**候选 3**（行业两层结构）去冲 brief §六验收线（年化 ≥20% / Sharpe ≥0.8 / MDD <35%）
- 候选 2、4 留作 M5+ 迭代

---

## 6. 调研的"负产出"

**未在调研中找到的东西**（避免将来重复查）：
- 中信、海通专做"A 股裸动量失败"的深度研报（**不存在**，他们只发因子跟踪周报）
- qlib 的次新股过滤现成实现（**没有**，qlib `data/filter.py` 只有 Name/Expression/Series 三种）
- qlib 的止损/止盈模块（**没有**，rule_strategy.py 只有 TWAP/SBB/AC 执行算法）
- zipline-cn 的活跃 A 股适配（**已停更**）
- 华泰 exp_wgt_return_3m/6m 的具体 IC 数字（**摘要层查不到，需下载原研报**）

---

## 7. 产出

- [x] 本调研报告
- [ ] 更新 [[../deliverables/strategy-selection.md|strategy-selection]] §八开放问题的 M4 决策
- [ ] 更新 [[m4-spike-results.md|m4-spike-results]] §10，标注"候选改造方向已因调研而作废"
- [ ] 新建 M4 正式版规格书 `m4-spec.md`（基于候选 1 或 3）

---

## 8. 关键参考链接

- 学术：清华白颢睿 2020《财经研究》
- BigQuant：`wiki/doc/vmpoW4sE1e`（全 A 动量分层回测）
- Zhihu：[反转因子深度解析](https://zhuanlan.zhihu.com/p/386661895)
- 申万宏源：[多周期动量与反转因子研究](https://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/lastest/rptid/768550409293/index.phtml)
- 聚宽：[修改行宽-偷鸡](https://www.joinquant.com/view/community/detail/9eafe20d40f7ad1fb52669370e1f9942)
- qlib：`github.com/microsoft/qlib`（Alpha158 / TopkDropoutStrategy / Exchange）
- hugo2046/QuantsPlaybook：研报复现库（波动率止损、RSRS 等）
- WorldQuant 101 Alphas：`yli188/WorldQuant_alpha101_code`

**wiki 查询结果**：本项目是 llm-wiki 第一批量化知识的起点。M5 复盘时把本报告沉淀到 `wiki/synthesis/a-share-quant-prior-art.md`。

---

## 9. 开源策略可抄性评估（追加调研）

触发问题："开源策略可以抄吗？它们都用什么引擎？"

**一句话结论**：**6 个项目一个都不能直接抄**，没有任何开源项目提供"A 股截面短期反转策略"的完整实现。

### 9.1 详细评估表

| # | 项目 | Stars/更新 | License | 引擎 | 数据源 | 有反转策略？ | 迁移难度 |
|---|---|---|---|---|---|---|---|
| 1 | microsoft/qlib | 42.3k / 2026-04 | MIT | 自研全栈 + TopkDropoutStrategy | qlib 私有 binary | **否** · 全是 ML 打分 | 难 · 自研引擎基本要推倒重来 |
| 2 | hugo2046/QuantsPlaybook | 5.0k / 2026-05 | 无 LICENSE | alphalens + pandas，部分调 Backtrader | JoinQuant 为主 | **部分** · 都是因子研究 notebook，**无 backtest 循环** | 中 · 抄公式不抄框架 |
| 3 | phonegapX/alphasickle | 397 / 2024-03 | 无 LICENSE | 纯 pandas + scipy linprog | Tushare | **否** · CSI300 指数增强不是排名选股 | 难 · 重写 |
| 4 | ricequant/rqalpha | 6.4k / 2026-04 | NOASSERTION | 自研事件驱动 | 绑定米筐 | **否** · examples 全是 CTA 择时 | 难 · API 不兼容 |
| 5 | yli188/WorldQuant_alpha101_code | 739 / 2019-03 | 无 LICENSE | **无回测** | 不绑定 | **否** · 只有公式 | 易（作为公式抄袭源）|
| 6a | tkfy920/qstock | 1.8k / 2025-03 | MIT | `vec_backtest.py` 开源 + `bt_backtest.py` 付费墙 | 东财/新浪公共接口 | **部分** · `MR_Strategy` 是单票均值回归不是截面反转 | 中 · 只能抄指标计算 |
| 6b | khscience/OSkhQuant | 1.2k / 2026-05 | **CC BY-NC 禁商用** | 自研 + miniQMT 依赖 | miniQMT 券商客户端 | **否** | 弃 |

### 9.2 三个"看起来像但别碰"的陷阱

| 陷阱 | 危险 |
|---|---|
| **qlib** | 42k stars 迷惑性最大。benchmark 的 Linear 模型在 Alpha158 上学**所有因子的线性组合打分**，不是反转策略。强耦合自己的 binary 数据格式，接 Tushare 的成本 > 自己写 |
| **qstock `MR_Strategy`** | 名字叫 Mean Reversion 容易误判为"截面反转"。实际是**单票**时间序列 z-score，抄过来得到错误结论 |
| **rqalpha** | 6.4k stars 最像生产级，但官方 `examples/` **全是 CTA 择时**（MACD/海龟/金叉），一个横截面都没有。API 与我们的 `strategy(asof, bars, portfolio)` 协议不兼容 |

### 9.3 可抄清单（分层）

按"即拿即用"到"要改造"排序：

1. **WorldQuant 101 Alphas 公式**（Alpha#4、#9、#12、#53 反转类）— 翻译 pandas ~10 行 / 个
2. **hugo2046 的两份研报 PDF + notebook**：
   - `开源证券-A股反转之力的微观来源`（M_high - M_low 因子）
   - `再论动量因子`（中期动量重构）
   - 读公式、不读框架
3. **qlib Alpha158 的因子定义** — 翻译 pandas 20-30 行
4. **qlib `is_stock_tradable` 三段式** — 算法常识 ~40 行
5. **qstock `trade_performance()`** — NAV/指标计算 180 行可参考

### 9.4 M3 "自研引擎" 决策再次验证

[[m3-decisions]] 当时选自研 vs qlib / Backtrader / rqalpha 的理由，在这次调研中**每一条都被印证**：

- qlib 的策略代码与我的 strategy 协议不同构 → 迁移等于重写
- rqalpha 官方不提供横截面策略 → 它适合 CTA，不适合因子选股
- 我的 350 行引擎**在开源生态里是独一份**（协议 = 每日收盘后纯函数返回目标权重）

**→ 继续走自研**。M4 正式版走候选 1（Spike B nlargest → nsmallest）。开源项目作为**公式来源**使用，不作为**框架依赖**。
