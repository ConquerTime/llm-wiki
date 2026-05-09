"""M4 Spike · 两种趋势形态对比。

规格：notes/m4-spike-spec.md
两个 Spike：
  A. 每日选全市场 20 日动量 Top1 满仓
  B. 每月选 Top10 等权（月频换仓）
共用：负过滤（ST/停牌/流动性底 20%/上市<250日/北交所）+ 样本期 2016-2026 + 基准 000300.SH

用法：
  python -m scripts.m4_spike --which both
  python -m scripts.m4_spike --which A --end 20180101   # 快速冒烟
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

# 实验脚本住 project 的 experiments/scripts/，引擎 2026-05-09 迁至 practices/quant-investing/engine/
# 实验产物仍落在本 project 的 experiments/data/（与 project 周期绑定，不污染 practice）
HERE = Path(__file__).resolve().parent         # experiments/scripts
ROOT = HERE.parent                             # experiments/（实验产物落点）
# 从 experiments/scripts/ 上溯到 vault 根再进 practices/...
VAULT_ROOT = HERE.parent.parent.parent.parent  # projects/X/deliverables/experiments/scripts -> vault
ENGINE_ROOT = VAULT_ROOT / "practices" / "quant-investing" / "engine"
sys.path.insert(0, str(ENGINE_ROOT))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from quant_data.api import get_bars  # noqa: E402
from quant_data.backtest import BacktestEngine, buy_and_hold_nav  # noqa: E402
from quant_data.backtest.metrics import summary, format_report  # noqa: E402
from quant_data.factors import momentum_n  # noqa: E402
from quant_data.universe import build_universe, negative_filter_asof  # noqa: E402
from quant_data.universe.filters import load_all_bars  # noqa: E402


def prepare_data(start: str, end: str | None, mom_n: int = 20) -> dict:
    """一次性加载全市场数据 + 预计算动量。"""
    t0 = time.time()
    print(f"[data] load_all_bars {start}-{end or 'latest'}...")
    bars_long = load_all_bars(start, end)
    print(f"  bars_long shape = {bars_long.shape}, 耗时 {time.time()-t0:.1f}s")

    t0 = time.time()
    # 剔除北交所 + ETF + 指数（510300.SH, 000300.SH）
    bars_long = bars_long[~bars_long["ts_code"].str.endswith(".BJ")]
    bars_long = bars_long[~bars_long["ts_code"].isin(["510300.SH", "000300.SH"])]
    print(f"  过滤 BJ + ETF/指数 后 shape = {bars_long.shape}, 耗时 {time.time()-t0:.1f}s")

    t0 = time.time()
    mom = momentum_n(bars_long, mom_n)
    print(f"  动量矩阵 shape = {mom.shape}, 耗时 {time.time()-t0:.1f}s")

    t0 = time.time()
    ctx = build_universe(start_date=start)
    print(f"  universe static loaded 耗时 {time.time()-t0:.1f}s")

    # 为引擎准备 dict 格式 bars
    # 只保留存在动量非空的 ts_code（上市 ≥ mom_n 天）
    t0 = time.time()
    codes_with_mom = set(mom.columns[(~mom.isna()).any()])
    bars_long = bars_long[bars_long["ts_code"].isin(codes_with_mom)]
    bars_dict = {
        code: df[["trade_date", "open", "high", "low", "close", "vol", "amount"]]
        for code, df in bars_long.groupby("ts_code")
    }
    print(f"  bars_dict 构建 {len(bars_dict)} 只，耗时 {time.time()-t0:.1f}s")

    # 每日 amount pivot 方便过滤
    t0 = time.time()
    amount_pvt = bars_long.pivot(index="trade_date", columns="ts_code", values="amount")
    amount_pvt = amount_pvt.sort_index()
    amount_pvt.index = pd.to_datetime(amount_pvt.index)
    print(f"  amount pivot shape = {amount_pvt.shape}, 耗时 {time.time()-t0:.1f}s")

    # 动量矩阵的 index 转 datetime
    mom.index = pd.to_datetime(mom.index)

    # 大盘趋势闸：HS300 收盘 vs SMA60
    t0 = time.time()
    hs300 = get_bars("000300.SH", start=start, end=end, adj="none")
    hs300 = hs300.set_index("trade_date").sort_index()
    hs300_sma60 = hs300["close"].rolling(60).mean()
    regime_on = (hs300["close"] > hs300_sma60)  # True = 允许开仓
    print(f"  HS300 趋势闸加载（60 日均线），开仓日占比 {regime_on.mean():.2%}, 耗时 {time.time()-t0:.1f}s")

    # close + ATR_14 矩阵（Spike G 的 ATR 止损用）
    t0 = time.time()
    close_pvt = bars_long.pivot(index="trade_date", columns="ts_code", values="close")
    close_pvt = close_pvt.sort_index()
    close_pvt.index = pd.to_datetime(close_pvt.index)
    high_pvt = bars_long.pivot(index="trade_date", columns="ts_code", values="high").sort_index()
    low_pvt  = bars_long.pivot(index="trade_date", columns="ts_code", values="low").sort_index()
    high_pvt.index = pd.to_datetime(high_pvt.index)
    low_pvt.index  = pd.to_datetime(low_pvt.index)
    prev_close = close_pvt.shift(1)
    tr = pd.concat([
        (high_pvt - low_pvt),
        (high_pvt - prev_close).abs(),
        (low_pvt  - prev_close).abs(),
    ]).groupby(level=0).max()
    atr14 = tr.rolling(14).mean()
    print(f"  close/ATR 矩阵（Spike G 止损用），耗时 {time.time()-t0:.1f}s")

    # 残差动量（Spike H 单窗 / Spike H3 多窗用）：
    #   对每只股票做 60 日滚动 OLS vs HS300 取 residual，再累加不同窗口
    t0 = time.time()
    stock_rets = close_pvt.pct_change()
    market_rets = hs300["close"].pct_change()
    market_rets.index = pd.to_datetime(market_rets.index)
    market_rets = market_rets.reindex(stock_rets.index)
    beta_window = 60
    var_m = market_rets.rolling(beta_window).var()
    cov_sm = stock_rets.rolling(beta_window).cov(market_rets)
    beta_roll = cov_sm.div(var_m, axis=0)
    residuals = stock_rets.sub(beta_roll.mul(market_rets, axis=0))
    # 单窗 20 日（Spike H 用）
    residual_mom = residuals.rolling(mom_n).sum()
    # 多窗 5/10/20（Spike H3 用）
    residual_mom_5  = residuals.rolling(5).sum()
    residual_mom_10 = residuals.rolling(10).sum()
    residual_mom_20 = residual_mom  # alias
    print(f"  残差动量（单窗 {mom_n}/多窗 5/10/20），shape {residual_mom.shape}，"
          f"耗时 {time.time()-t0:.1f}s")

    # 行业映射 + 行业动量（用于 Spike F 及以后）
    t0 = time.time()
    import duckdb
    from quant_data.config import CONFIG
    con = duckdb.connect(str(CONFIG.db_path), read_only=True)
    ind_df = con.execute(
        "SELECT ts_code, industry FROM stock_basic WHERE list_status='L' AND industry IS NOT NULL"
    ).df()
    con.close()
    ind_map = dict(zip(ind_df["ts_code"], ind_df["industry"]))
    # 行业动量：把个股 mom_n 按行业等权平均
    mom_long = mom.stack().rename("mom").reset_index()
    mom_long.columns = ["trade_date", "ts_code", "mom"]
    mom_long["industry"] = mom_long["ts_code"].map(ind_map)
    mom_long = mom_long.dropna(subset=["industry"])
    industry_mom = (
        mom_long.groupby(["trade_date", "industry"])["mom"].mean().unstack()
    )
    print(f"  行业映射 + 行业动量：{len(set(ind_map.values()))} 个行业，"
          f"industry_mom shape {industry_mom.shape}，耗时 {time.time()-t0:.1f}s")

    return {
        "bars_dict": bars_dict,
        "mom": mom,
        "amount_pvt": amount_pvt,
        "ctx": ctx,
        "regime_on": regime_on,
        "ind_map": ind_map,
        "industry_mom": industry_mom,
        "close_pvt": close_pvt,
        "atr14": atr14,
        "residual_mom": residual_mom,
        "residual_mom_5": residual_mom_5,
        "residual_mom_10": residual_mom_10,
        "residual_mom_20": residual_mom_20,
    }


def make_spike_a_strategy(data: dict, mom_n: int = 20):
    """单票 Top1 动量：每日选全市场动量最强的那只股票满仓。"""
    mom = data["mom"]
    amount_pvt = data["amount_pvt"]
    ctx = data["ctx"]

    def strat(asof: pd.Timestamp, bars, portfolio):
        if asof not in mom.index:
            return {}
        # 当日动量行
        mom_row = mom.loc[asof].dropna()
        if mom_row.empty:
            return {}
        # 负过滤
        today_amount = amount_pvt.loc[asof].dropna() if asof in amount_pvt.index else pd.Series()
        bars_today = pd.DataFrame({
            "ts_code": today_amount.index,
            "amount": today_amount.values,
        })
        eligible = set(negative_filter_asof(ctx, asof, bars_today=bars_today))
        mom_row = mom_row[mom_row.index.isin(eligible)]
        if mom_row.empty:
            return {}
        # 只取动量为正的前 1 名（避免全市场都跌时硬买）
        positive = mom_row[mom_row > 0]
        if positive.empty:
            return {}  # 全市场动量皆负 → 空仓
        top1 = positive.idxmax()
        return {top1: 1.0}
    return strat


def make_spike_b_strategy(data: dict, mom_n: int = 20, top_k: int = 10,
                           rebalance_interval: int = 20):
    """横截面 Top-K 等权，月频（20 交易日）换仓。"""
    mom = data["mom"]
    amount_pvt = data["amount_pvt"]
    ctx = data["ctx"]
    state = {"last_rebalance": None, "last_weights": {}}

    def strat(asof: pd.Timestamp, bars, portfolio):
        last = state["last_rebalance"]
        # 每 N 个交易日才动
        if last is not None:
            # 判断是否到了换仓日
            trade_dates = mom.index
            try:
                idx_last = trade_dates.get_loc(last)
                idx_now  = trade_dates.get_loc(asof)
            except KeyError:
                return state["last_weights"]
            if idx_now - idx_last < rebalance_interval:
                return state["last_weights"]
        # 到了换仓日
        if asof not in mom.index:
            return state["last_weights"]
        mom_row = mom.loc[asof].dropna()
        today_amount = amount_pvt.loc[asof].dropna() if asof in amount_pvt.index else pd.Series()
        bars_today = pd.DataFrame({
            "ts_code": today_amount.index,
            "amount": today_amount.values,
        })
        eligible = set(negative_filter_asof(ctx, asof, bars_today=bars_today))
        mom_row = mom_row[mom_row.index.isin(eligible)]
        positive = mom_row[mom_row > 0]
        if positive.empty:
            state["last_weights"] = {}
            state["last_rebalance"] = asof
            return {}
        top = positive.nlargest(top_k)
        w = 1.0 / len(top)
        weights = {code: w for code in top.index}
        state["last_weights"] = weights
        state["last_rebalance"] = asof
        return weights
    return strat


def make_spike_d_strategy(data: dict, mom_n: int = 20, top_k: int = 10,
                           rebalance_interval: int = 20):
    """Spike D · 反转版：买过去 N 日跌幅最大的 Top-K，月频换仓等权。

    与 Spike B 仅有两点差异：
      - 筛选 mom_row < 0（下跌股）而不是 > 0
      - nsmallest 取最负值（跌得最多的）
    其他逻辑（月频换仓、负过滤池、状态管理）完全照搬。
    """
    mom = data["mom"]
    amount_pvt = data["amount_pvt"]
    ctx = data["ctx"]
    state = {"last_rebalance": None, "last_weights": {}}

    def strat(asof: pd.Timestamp, bars, portfolio):
        last = state["last_rebalance"]
        if last is not None:
            trade_dates = mom.index
            try:
                idx_last = trade_dates.get_loc(last)
                idx_now  = trade_dates.get_loc(asof)
            except KeyError:
                return state["last_weights"]
            if idx_now - idx_last < rebalance_interval:
                return state["last_weights"]
        if asof not in mom.index:
            return state["last_weights"]
        mom_row = mom.loc[asof].dropna()
        today_amount = amount_pvt.loc[asof].dropna() if asof in amount_pvt.index else pd.Series()
        bars_today = pd.DataFrame({
            "ts_code": today_amount.index,
            "amount": today_amount.values,
        })
        eligible = set(negative_filter_asof(ctx, asof, bars_today=bars_today))
        mom_row = mom_row[mom_row.index.isin(eligible)]
        negative = mom_row[mom_row < 0]
        if negative.empty:
            # 全市场都在涨 → 空仓（反向对应原版"全市场都在跌则空仓"）
            state["last_weights"] = {}
            state["last_rebalance"] = asof
            return {}
        bottom = negative.nsmallest(top_k)
        w = 1.0 / len(bottom)
        weights = {code: w for code in bottom.index}
        state["last_weights"] = weights
        state["last_rebalance"] = asof
        return weights
    return strat


def make_spike_h3_strategy(data: dict, mom_n: int = 20,
                            top_industries: int = 10, top_per_industry: int = 1,
                            rebalance_interval: int = 20):
    """Spike H3 · H 的内层信号换成多窗合成（5/10/20 残差动量，rank 等权）。

    为什么不用 raw 加权：三窗尺度差 4x（20 日累计 ≈ 5 日累计的 4 倍），
    raw sum 会给短窗 1/4 权重。rank 化让三窗等地位参与。

    调研指示：10 日反转 IC 0.051（最强），20 日 0.038，60 日归零。
    先用等权验证"多窗 > 单窗"，权重优化留给 M5+。
    """
    mom = data["mom"]
    rm5  = data["residual_mom_5"]
    rm10 = data["residual_mom_10"]
    rm20 = data["residual_mom_20"]
    amount_pvt = data["amount_pvt"]
    ctx = data["ctx"]
    regime_on = data["regime_on"]
    ind_map = data["ind_map"]
    industry_mom = data["industry_mom"]
    state = {"last_rebalance": None, "last_weights": {}}

    def strat(asof: pd.Timestamp, bars, portfolio):
        if asof in regime_on.index and bool(regime_on.loc[asof]):
            state["last_weights"] = {}
            return {}

        last = state["last_rebalance"]
        if last is not None:
            trade_dates = mom.index
            try:
                idx_last = trade_dates.get_loc(last)
                idx_now  = trade_dates.get_loc(asof)
            except KeyError:
                return state["last_weights"]
            if idx_now - idx_last < rebalance_interval:
                return state["last_weights"]

        # 外层：用原 industry_mom 选跌最多的行业
        if asof not in industry_mom.index:
            return state["last_weights"]
        ind_row = industry_mom.loc[asof].dropna()
        ind_neg = ind_row[ind_row < 0]
        if ind_neg.empty:
            state["last_weights"] = {}
            state["last_rebalance"] = asof
            return {}
        selected_industries = set(ind_neg.nsmallest(top_industries).index)

        # 内层：合成 rank（三窗 ascending rank 等权平均；rank 越小=反转信号越强）
        if asof not in rm5.index or asof not in rm10.index or asof not in rm20.index:
            return state["last_weights"]
        r5  = rm5.loc[asof].rank(ascending=True)
        r10 = rm10.loc[asof].rank(ascending=True)
        r20 = rm20.loc[asof].rank(ascending=True)
        # 三窗都有值才算合成 rank
        combined = pd.concat([r5, r10, r20], axis=1).dropna().mean(axis=1)
        if combined.empty:
            return state["last_weights"]

        today_amount = amount_pvt.loc[asof].dropna() if asof in amount_pvt.index else pd.Series()
        bars_today = pd.DataFrame({
            "ts_code": today_amount.index,
            "amount": today_amount.values,
        })
        eligible = set(negative_filter_asof(ctx, asof, bars_today=bars_today))
        combined = combined[combined.index.isin(eligible)]
        cand_inds = pd.Series({c: ind_map.get(c) for c in combined.index})
        cand_inds = cand_inds[cand_inds.isin(selected_industries)]
        combined = combined[combined.index.isin(cand_inds.index)]

        # 内层：每个行业按合成 rank 升序选 Top K
        # 反转：rank 越小（值越负 / 跌得越狠）越优先选
        # 但"跌幅为正的股票"不该被选 → 检查原始值是否 < 0
        # 简化：rank 已经按值升序，只取 rank 低的几个就等价于最负
        picks: list[str] = []
        for ind_name in selected_industries:
            members = cand_inds[cand_inds == ind_name].index
            m = combined[combined.index.isin(members)]
            if m.empty:
                continue
            # 用原始 residual_mom_10 判断是否"确实在跌"（避免全市场都涨时的误选）
            r10_members = rm10.loc[asof, members].dropna()
            neg_members = set(r10_members[r10_members < 0].index)
            m = m[m.index.isin(neg_members)]
            if m.empty:
                continue
            picks.extend(m.nsmallest(top_per_industry).index.tolist())

        if not picks:
            state["last_weights"] = {}
            state["last_rebalance"] = asof
            return {}
        w = 1.0 / len(picks)
        weights = {code: w for code in picks}
        state["last_weights"] = weights
        state["last_rebalance"] = asof
        return weights
    return strat


def make_spike_h_strategy(data: dict, mom_n: int = 20,
                           top_industries: int = 10, top_per_industry: int = 1,
                           rebalance_interval: int = 20):
    """Spike H · F 的内层信号换成残差反转（剥离市场 beta）。

    差异**仅在内层选股**：
      - F: 内层按原始 mom（过去 N 日价格收益）升序选 K
      - H: 内层按残差 mom（过去 N 日去市场 beta 后的累计残差）升序选 K
    其他（外层行业动量、反向闸、月频、Top M×K）与 F 完全一致。

    目的：残差把"因为大盘跌所以跌的股票"剥掉，只留"相对跑输同一市场状态下其他股票的"。
    预期改善：单边牛市年（2017/2019/2020）不再把"跌得少因为牛市"误判为反转候选。
    """
    mom = data["mom"]
    residual_mom = data["residual_mom"]
    amount_pvt = data["amount_pvt"]
    ctx = data["ctx"]
    regime_on = data["regime_on"]
    ind_map = data["ind_map"]
    industry_mom = data["industry_mom"]
    state = {"last_rebalance": None, "last_weights": {}}

    def strat(asof: pd.Timestamp, bars, portfolio):
        if asof in regime_on.index and bool(regime_on.loc[asof]):
            state["last_weights"] = {}
            return {}

        last = state["last_rebalance"]
        if last is not None:
            trade_dates = mom.index
            try:
                idx_last = trade_dates.get_loc(last)
                idx_now  = trade_dates.get_loc(asof)
            except KeyError:
                return state["last_weights"]
            if idx_now - idx_last < rebalance_interval:
                return state["last_weights"]

        # 外层：仍用原 industry_mom 选跌最多的行业（行业层不做残差）
        if asof not in industry_mom.index:
            return state["last_weights"]
        ind_row = industry_mom.loc[asof].dropna()
        ind_neg = ind_row[ind_row < 0]
        if ind_neg.empty:
            state["last_weights"] = {}
            state["last_rebalance"] = asof
            return {}
        selected_industries = set(ind_neg.nsmallest(top_industries).index)

        # 内层：用 residual_mom 选
        if asof not in residual_mom.index:
            return state["last_weights"]
        rm_row = residual_mom.loc[asof].dropna()
        today_amount = amount_pvt.loc[asof].dropna() if asof in amount_pvt.index else pd.Series()
        bars_today = pd.DataFrame({
            "ts_code": today_amount.index,
            "amount": today_amount.values,
        })
        eligible = set(negative_filter_asof(ctx, asof, bars_today=bars_today))
        rm_row = rm_row[rm_row.index.isin(eligible)]
        cand_inds = pd.Series({c: ind_map.get(c) for c in rm_row.index})
        cand_inds = cand_inds[cand_inds.isin(selected_industries)]
        rm_row = rm_row[rm_row.index.isin(cand_inds.index)]

        picks: list[str] = []
        for ind_name in selected_industries:
            members = cand_inds[cand_inds == ind_name].index
            m = rm_row[rm_row.index.isin(members)]
            m_neg = m[m < 0]
            if m_neg.empty:
                continue
            picks.extend(m_neg.nsmallest(top_per_industry).index.tolist())

        if not picks:
            state["last_weights"] = {}
            state["last_rebalance"] = asof
            return {}
        w = 1.0 / len(picks)
        weights = {code: w for code in picks}
        state["last_weights"] = weights
        state["last_rebalance"] = asof
        return weights
    return strat


def make_spike_g_strategy(data: dict, mom_n: int = 20,
                           top_industries: int = 10, top_per_industry: int = 1,
                           rebalance_interval: int = 20,
                           atr_mult: float = 2.0):
    """Spike G · F + ATR 止损。

    差异仅在"每日持仓检查"这一层：
      - 每次调用先看所有持仓是否跌破 entry_price - atr_mult * atr_at_entry
      - 触发止损的 code 从 last_weights 踢出（引擎按新 weights 卖掉）
      - 止损后不补仓，等下次月度换仓
      - 换仓日买入时记录 entry_price（用 close 近似买入价，买入成交实际在次日 open，
        精度损失 < 1 天差，可接受）

    其他（反向闸、月频、行业两层选股）与 F 完全一致。
    """
    mom = data["mom"]
    amount_pvt = data["amount_pvt"]
    ctx = data["ctx"]
    regime_on = data["regime_on"]
    ind_map = data["ind_map"]
    industry_mom = data["industry_mom"]
    close_pvt = data["close_pvt"]
    atr14 = data["atr14"]
    # state.entry: {ts_code -> (entry_price, atr_at_entry)}
    state = {"last_rebalance": None, "last_weights": {}, "entry": {}}

    def _check_stops(asof: pd.Timestamp) -> set[str]:
        """返回当日触发止损的 ts_code 集合。"""
        stopped = set()
        if not state["entry"]:
            return stopped
        if asof not in close_pvt.index:
            return stopped
        today_close = close_pvt.loc[asof]
        for code, (entry_price, atr_entry) in state["entry"].items():
            c = today_close.get(code)
            if pd.isna(c) or c is None:
                continue
            stop_line = entry_price - atr_mult * atr_entry
            if c < stop_line:
                stopped.add(code)
        return stopped

    def strat(asof: pd.Timestamp, bars, portfolio):
        # 反向闸：牛市空仓（沿用 E/F）
        if asof in regime_on.index and bool(regime_on.loc[asof]):
            state["last_weights"] = {}
            state["entry"].clear()  # 空仓 → 清除 entry 记录
            return {}

        # 每日：先检查止损
        stopped = _check_stops(asof)
        if stopped:
            for code in stopped:
                state["entry"].pop(code, None)
            new_weights = {k: v for k, v in state["last_weights"].items() if k not in stopped}
            state["last_weights"] = new_weights
            # 止损后继续往下走：如果今天是换仓日，仍要按 F 逻辑重选

        last = state["last_rebalance"]
        if last is not None:
            trade_dates = mom.index
            try:
                idx_last = trade_dates.get_loc(last)
                idx_now  = trade_dates.get_loc(asof)
            except KeyError:
                return state["last_weights"]
            if idx_now - idx_last < rebalance_interval:
                # 非换仓日：返回当前权重（已踢出止损）
                return state["last_weights"]

        # 换仓日：跑 F 的选股逻辑
        if asof not in mom.index or asof not in industry_mom.index:
            return state["last_weights"]
        ind_row = industry_mom.loc[asof].dropna()
        ind_neg = ind_row[ind_row < 0]
        if ind_neg.empty:
            state["last_weights"] = {}
            state["entry"].clear()
            state["last_rebalance"] = asof
            return {}
        selected_industries = set(ind_neg.nsmallest(top_industries).index)

        mom_row = mom.loc[asof].dropna()
        today_amount = amount_pvt.loc[asof].dropna() if asof in amount_pvt.index else pd.Series()
        bars_today = pd.DataFrame({
            "ts_code": today_amount.index,
            "amount": today_amount.values,
        })
        eligible = set(negative_filter_asof(ctx, asof, bars_today=bars_today))
        mom_row = mom_row[mom_row.index.isin(eligible)]
        cand_inds = pd.Series({c: ind_map.get(c) for c in mom_row.index})
        cand_inds = cand_inds[cand_inds.isin(selected_industries)]
        mom_row = mom_row[mom_row.index.isin(cand_inds.index)]

        picks: list[str] = []
        for ind_name in selected_industries:
            members = cand_inds[cand_inds == ind_name].index
            m = mom_row[mom_row.index.isin(members)]
            m_neg = m[m < 0]
            if m_neg.empty:
                continue
            picks.extend(m_neg.nsmallest(top_per_industry).index.tolist())

        if not picks:
            state["last_weights"] = {}
            state["entry"].clear()
            state["last_rebalance"] = asof
            return {}
        w = 1.0 / len(picks)
        weights = {code: w for code in picks}

        # 更新 entry 记录：只给新加入的 code 设 entry（老的保留，保持止损基准稳定）
        today_close = close_pvt.loc[asof] if asof in close_pvt.index else None
        today_atr   = atr14.loc[asof] if asof in atr14.index else None
        new_entry = {}
        for code in weights:
            if code in state["entry"]:
                new_entry[code] = state["entry"][code]  # 保留原 entry
            else:
                if today_close is None or today_atr is None:
                    continue
                c = today_close.get(code)
                a = today_atr.get(code)
                if pd.isna(c) or pd.isna(a):
                    continue
                new_entry[code] = (float(c), float(a))
        state["entry"] = new_entry
        state["last_weights"] = weights
        state["last_rebalance"] = asof
        return weights
    return strat


def make_spike_f_strategy(data: dict, mom_n: int = 20,
                           top_industries: int = 10, top_per_industry: int = 1,
                           rebalance_interval: int = 20):
    """Spike F · 行业两层反转：外层选"跌最狠的 M 个行业"，内层选"行业内跌最狠的 K 只"。

    与 Spike E 的差异**仅在选股层**（闸门、月频、反转方向都沿用）：
      - E: 全市场按 mom_n 升序选 Top K
      - F: 先按行业 mom_n 等权升序选 Top M 行业 → 再行业内按 mom_n 升序选 Top K
      - 总持仓 = M × K 只，等权

    默认 M=10, K=1 → 总持仓 10 只，与 E 的 Top 10 规模一致可对照。
    """
    mom = data["mom"]
    amount_pvt = data["amount_pvt"]
    ctx = data["ctx"]
    regime_on = data["regime_on"]
    ind_map = data["ind_map"]
    industry_mom = data["industry_mom"]
    state = {"last_rebalance": None, "last_weights": {}}

    def strat(asof: pd.Timestamp, bars, portfolio):
        # 反向闸：牛市空仓（沿用 E）
        if asof in regime_on.index and bool(regime_on.loc[asof]):
            state["last_weights"] = {}
            return {}

        last = state["last_rebalance"]
        if last is not None:
            trade_dates = mom.index
            try:
                idx_last = trade_dates.get_loc(last)
                idx_now  = trade_dates.get_loc(asof)
            except KeyError:
                return state["last_weights"]
            if idx_now - idx_last < rebalance_interval:
                return state["last_weights"]
        if asof not in mom.index:
            return state["last_weights"]

        # 1. 外层：选"跌最狠"的 M 个行业
        if asof not in industry_mom.index:
            return state["last_weights"]
        ind_row = industry_mom.loc[asof].dropna()
        ind_neg = ind_row[ind_row < 0]
        if ind_neg.empty:
            state["last_weights"] = {}
            state["last_rebalance"] = asof
            return {}
        selected_industries = set(ind_neg.nsmallest(top_industries).index)

        # 2. 内层：行业内按个股 mom_n 升序选 Top K
        mom_row = mom.loc[asof].dropna()
        today_amount = amount_pvt.loc[asof].dropna() if asof in amount_pvt.index else pd.Series()
        bars_today = pd.DataFrame({
            "ts_code": today_amount.index,
            "amount": today_amount.values,
        })
        eligible = set(negative_filter_asof(ctx, asof, bars_today=bars_today))
        # 限制在"合格池 ∩ 所选行业"
        mom_row = mom_row[mom_row.index.isin(eligible)]
        cand_inds = pd.Series({c: ind_map.get(c) for c in mom_row.index})
        cand_inds = cand_inds[cand_inds.isin(selected_industries)]
        mom_row = mom_row[mom_row.index.isin(cand_inds.index)]

        # 3. 每个行业内选 K 只跌幅最大
        picks: list[str] = []
        for ind_name in selected_industries:
            members = cand_inds[cand_inds == ind_name].index
            m = mom_row[mom_row.index.isin(members)]
            m_neg = m[m < 0]
            if m_neg.empty:
                continue
            picks.extend(m_neg.nsmallest(top_per_industry).index.tolist())

        if not picks:
            state["last_weights"] = {}
            state["last_rebalance"] = asof
            return {}
        w = 1.0 / len(picks)
        weights = {code: w for code in picks}
        state["last_weights"] = weights
        state["last_rebalance"] = asof
        return weights
    return strat


def make_spike_e_strategy(data: dict, mom_n: int = 20, top_k: int = 10,
                           rebalance_interval: int = 20):
    """Spike E · 反转 + 反向趋势闸：HS300 < SMA60（震荡/熊）才开仓，否则立即空仓。

    = Spike D 选股 + Spike C 闸门**反向**。
    逻辑：裸反转在单边牛市溃败（BigQuant 震荡 ICIR +0.45、牛市 -0.36），所以
    牛市时强制空仓，只在震荡/熊市做反转。
    """
    mom = data["mom"]
    amount_pvt = data["amount_pvt"]
    ctx = data["ctx"]
    regime_on = data["regime_on"]  # True = HS300 > SMA60（牛市）
    state = {"last_rebalance": None, "last_weights": {}}

    def strat(asof: pd.Timestamp, bars, portfolio):
        # 反向闸：牛市（regime_on=True）关闸空仓
        if asof in regime_on.index and bool(regime_on.loc[asof]):
            state["last_weights"] = {}
            return {}

        last = state["last_rebalance"]
        if last is not None:
            trade_dates = mom.index
            try:
                idx_last = trade_dates.get_loc(last)
                idx_now  = trade_dates.get_loc(asof)
            except KeyError:
                return state["last_weights"]
            if idx_now - idx_last < rebalance_interval:
                return state["last_weights"]
        if asof not in mom.index:
            return state["last_weights"]
        mom_row = mom.loc[asof].dropna()
        today_amount = amount_pvt.loc[asof].dropna() if asof in amount_pvt.index else pd.Series()
        bars_today = pd.DataFrame({
            "ts_code": today_amount.index,
            "amount": today_amount.values,
        })
        eligible = set(negative_filter_asof(ctx, asof, bars_today=bars_today))
        mom_row = mom_row[mom_row.index.isin(eligible)]
        negative = mom_row[mom_row < 0]
        if negative.empty:
            state["last_weights"] = {}
            state["last_rebalance"] = asof
            return {}
        bottom = negative.nsmallest(top_k)
        w = 1.0 / len(bottom)
        weights = {code: w for code in bottom.index}
        state["last_weights"] = weights
        state["last_rebalance"] = asof
        return weights
    return strat


def make_spike_c_strategy(data: dict, mom_n: int = 20, top_k: int = 10,
                           rebalance_interval: int = 20):
    """Spike B + 大盘趋势闸：HS300 > SMA60 才开仓，否则立即空仓。

    与 B 的区别只在"闸关时立即清仓"——不等下一次换仓日。
    """
    mom = data["mom"]
    amount_pvt = data["amount_pvt"]
    ctx = data["ctx"]
    regime_on = data["regime_on"]
    state = {"last_rebalance": None, "last_weights": {}}

    def strat(asof: pd.Timestamp, bars, portfolio):
        # 闸门优先：关闸立即空仓（覆盖月频节奏）
        if asof in regime_on.index and not bool(regime_on.loc[asof]):
            state["last_weights"] = {}
            return {}

        last = state["last_rebalance"]
        if last is not None:
            trade_dates = mom.index
            try:
                idx_last = trade_dates.get_loc(last)
                idx_now  = trade_dates.get_loc(asof)
            except KeyError:
                return state["last_weights"]
            if idx_now - idx_last < rebalance_interval:
                return state["last_weights"]
        if asof not in mom.index:
            return state["last_weights"]
        mom_row = mom.loc[asof].dropna()
        today_amount = amount_pvt.loc[asof].dropna() if asof in amount_pvt.index else pd.Series()
        bars_today = pd.DataFrame({
            "ts_code": today_amount.index,
            "amount": today_amount.values,
        })
        eligible = set(negative_filter_asof(ctx, asof, bars_today=bars_today))
        mom_row = mom_row[mom_row.index.isin(eligible)]
        positive = mom_row[mom_row > 0]
        if positive.empty:
            state["last_weights"] = {}
            state["last_rebalance"] = asof
            return {}
        top = positive.nlargest(top_k)
        w = 1.0 / len(top)
        weights = {code: w for code in top.index}
        state["last_weights"] = weights
        state["last_rebalance"] = asof
        return weights
    return strat


def run_one(name: str, strat_fn, data: dict, start_cash: float, start: str, end: str | None):
    print(f"\n[{name}] 启动引擎...")
    t0 = time.time()
    engine = BacktestEngine(
        data["bars_dict"], strat_fn,
        start_cash=start_cash,
        start_date=start, end_date=end,
        fast_mode=True,
    )
    print(f"  引擎构造完成，耗时 {time.time()-t0:.1f}s")
    t0 = time.time()
    res = engine.run()
    print(f"  回测完成，耗时 {time.time()-t0:.1f}s")
    return res


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--which", default="both",
                        choices=["A", "B", "C", "D", "E", "F", "G", "H", "H3",
                                 "both", "BC", "BD", "BCD", "DE", "BCDE",
                                 "EF", "DEF", "FG", "EFG", "FH", "FGH",
                                 "HH3", "FHH3"])
    parser.add_argument("--top-industries", type=int, default=10,
                        help="Spike F/G 外层：选 M 个行业")
    parser.add_argument("--top-per-industry", type=int, default=1,
                        help="Spike F/G 内层：每行业选 K 只")
    parser.add_argument("--atr-mult", type=float, default=2.0,
                        help="Spike G ATR 止损倍数（默认 2.0）")
    parser.add_argument("--start", default="20160101")
    parser.add_argument("--end", default=None)
    parser.add_argument("--mom-n", type=int, default=20)
    parser.add_argument("--cash", type=float, default=1_000_000.0)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--rebalance", type=int, default=20)
    args = parser.parse_args()

    data = prepare_data(args.start, args.end, args.mom_n)

    # 基准：000300.SH
    print("\n[基准] 加载 000300.SH ...")
    bench_df = get_bars("000300.SH", start=args.start, end=args.end, adj="none")
    bench_nav = buy_and_hold_nav(bench_df)

    results = {}

    if args.which in ("A", "both"):
        res_a = run_one("Spike A", make_spike_a_strategy(data, args.mom_n),
                        data, args.cash, args.start, args.end)
        m_a = summary(res_a.nav, benchmark=bench_nav, trades=res_a.trades,
                      equity=res_a.daily["equity"])
        print("\n=== Spike A · 单票 Top1 动量 ===")
        print(format_report(m_a))
        results["A"] = (res_a, m_a)
        _dump("A", res_a, m_a, bench_nav, args)

    if args.which in ("B", "both", "BC"):
        res_b = run_one("Spike B", make_spike_b_strategy(data, args.mom_n, args.top_k, args.rebalance),
                        data, args.cash, args.start, args.end)
        m_b = summary(res_b.nav, benchmark=bench_nav, trades=res_b.trades,
                      equity=res_b.daily["equity"])
        print(f"\n=== Spike B · 横截面 Top-{args.top_k} 月频 ===")
        print(format_report(m_b))
        results["B"] = (res_b, m_b)
        _dump("B", res_b, m_b, bench_nav, args)

    if args.which in ("C", "BC", "BCD"):
        res_c = run_one("Spike C", make_spike_c_strategy(data, args.mom_n, args.top_k, args.rebalance),
                        data, args.cash, args.start, args.end)
        m_c = summary(res_c.nav, benchmark=bench_nav, trades=res_c.trades,
                      equity=res_c.daily["equity"])
        print(f"\n=== Spike C · B + HS300 趋势闸（SMA60）===")
        print(format_report(m_c))
        results["C"] = (res_c, m_c)
        _dump("C", res_c, m_c, bench_nav, args)

    if args.which in ("D", "BD", "BCD", "DE", "BCDE"):
        res_d = run_one("Spike D", make_spike_d_strategy(data, args.mom_n, args.top_k, args.rebalance),
                        data, args.cash, args.start, args.end)
        m_d = summary(res_d.nav, benchmark=bench_nav, trades=res_d.trades,
                      equity=res_d.daily["equity"])
        print(f"\n=== Spike D · 反转版 Top-{args.top_k} 月频（买过去 {args.mom_n} 日跌幅最大）===")
        print(format_report(m_d))
        results["D"] = (res_d, m_d)
        _dump("D", res_d, m_d, bench_nav, args)

    if args.which in ("E", "DE", "BCDE", "EF"):
        res_e = run_one("Spike E", make_spike_e_strategy(data, args.mom_n, args.top_k, args.rebalance),
                        data, args.cash, args.start, args.end)
        m_e = summary(res_e.nav, benchmark=bench_nav, trades=res_e.trades,
                      equity=res_e.daily["equity"])
        print(f"\n=== Spike E · D + 反向 HS300 闸门（牛市空仓 / 震荡做反转）===")
        print(format_report(m_e))
        results["E"] = (res_e, m_e)
        _dump("E", res_e, m_e, bench_nav, args)

    if args.which in ("F", "EF", "DEF", "FG", "EFG"):
        res_f = run_one("Spike F", make_spike_f_strategy(
            data, args.mom_n, args.top_industries, args.top_per_industry, args.rebalance),
                        data, args.cash, args.start, args.end)
        m_f = summary(res_f.nav, benchmark=bench_nav, trades=res_f.trades,
                      equity=res_f.daily["equity"])
        print(f"\n=== Spike F · 行业两层反转（外 {args.top_industries} 行业 × 内 {args.top_per_industry} 股 + 反向闸门）===")
        print(format_report(m_f))
        results["F"] = (res_f, m_f)
        _dump("F", res_f, m_f, bench_nav, args)

    if args.which in ("G", "FG", "EFG"):
        res_g = run_one("Spike G", make_spike_g_strategy(
            data, args.mom_n, args.top_industries, args.top_per_industry,
            args.rebalance, args.atr_mult),
                        data, args.cash, args.start, args.end)
        m_g = summary(res_g.nav, benchmark=bench_nav, trades=res_g.trades,
                      equity=res_g.daily["equity"])
        print(f"\n=== Spike G · F + ATR{args.atr_mult:.1f} 止损 ===")
        print(format_report(m_g))
        results["G"] = (res_g, m_g)
        _dump("G", res_g, m_g, bench_nav, args)

    if args.which in ("H", "FH", "FGH", "HH3", "FHH3"):
        res_h = run_one("Spike H", make_spike_h_strategy(
            data, args.mom_n, args.top_industries, args.top_per_industry, args.rebalance),
                        data, args.cash, args.start, args.end)
        m_h = summary(res_h.nav, benchmark=bench_nav, trades=res_h.trades,
                      equity=res_h.daily["equity"])
        print(f"\n=== Spike H · F 内层改残差反转（60 日滚动 vs HS300 beta）===")
        print(format_report(m_h))
        results["H"] = (res_h, m_h)
        _dump("H", res_h, m_h, bench_nav, args)

    if args.which in ("H3", "HH3", "FHH3"):
        res_h3 = run_one("Spike H3", make_spike_h3_strategy(
            data, args.mom_n, args.top_industries, args.top_per_industry, args.rebalance),
                        data, args.cash, args.start, args.end)
        m_h3 = summary(res_h3.nav, benchmark=bench_nav, trades=res_h3.trades,
                       equity=res_h3.daily["equity"])
        print(f"\n=== Spike H3 · 多窗残差反转（5/10/20 rank 等权）===")
        print(format_report(m_h3))
        results["H3"] = (res_h3, m_h3)
        _dump("H3", res_h3, m_h3, bench_nav, args)

    return 0


def _dump(tag: str, res, metrics, bench_nav, args):
    out_json = ROOT / "data" / f"m4_spike_{tag}.json"
    out_csv  = ROOT / "data" / f"m4_spike_{tag}.csv"
    (ROOT / "data").mkdir(parents=True, exist_ok=True)
    payload = {
        "tag": tag, "args": vars(args), "metrics": metrics,
        "n_trades": int(len(res.trades)),
    }
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str),
                        encoding="utf-8")
    pd.DataFrame({
        "date": res.nav.index,
        "nav_strategy": res.nav.values,
        "nav_benchmark": bench_nav.reindex(res.nav.index).ffill().values,
    }).to_csv(out_csv, index=False)
    print(f"  JSON -> {out_json}")
    print(f"  CSV  -> {out_csv}")


if __name__ == "__main__":
    sys.exit(main())
