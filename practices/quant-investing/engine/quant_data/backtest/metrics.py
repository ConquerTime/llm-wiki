"""回测评价指标。

输入：
  nav: pd.Series，index=date，起始值不要求为 1（内部会归一化）
  benchmark: 可选的基准 NAV
  trades: 可选的交易明细 DataFrame

输出 dict：
  annual_return / annual_vol / sharpe / mdd / calmar / turnover / n_trades
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252
RISK_FREE = 0.02


def buy_and_hold_nav(bars_df: pd.DataFrame, price_col: str = "close") -> pd.Series:
    """把任意 bars DataFrame 转成 "首日 = 1.0 的买入持有 NAV Series"。

    用作 summary(benchmark=...) 的输入。支持"策略跑 X，基准画 Y"的场景：
        strat_res = BacktestEngine({"X": bars_x}, strat).run()
        bench = buy_and_hold_nav(bars_y)
        summary(strat_res.nav, benchmark=bench, ...)

    输入：
      bars_df: 含 trade_date + price_col 的 DataFrame
      price_col: 默认 close；若 bars 已前复权就用 close，否则改 'adj_close' 等
    """
    if bars_df is None or bars_df.empty:
        return pd.Series(dtype=float)
    d = bars_df.copy()
    if not pd.api.types.is_datetime64_any_dtype(d["trade_date"]):
        d["trade_date"] = pd.to_datetime(d["trade_date"])
    d = d.set_index("trade_date").sort_index()
    return d[price_col] / d[price_col].iloc[0]


def _annualize(nav: pd.Series) -> tuple[float, float, float]:
    """返回 (年化收益, 年化波动, 总天数)。"""
    if len(nav) < 2:
        return 0.0, 0.0, 0.0
    n = len(nav) - 1
    cum = nav.iloc[-1] / nav.iloc[0]
    years = n / TRADING_DAYS_PER_YEAR
    annual_ret = cum ** (1 / years) - 1 if years > 0 else 0.0
    daily_ret = nav.pct_change().dropna()
    annual_vol = daily_ret.std() * math.sqrt(TRADING_DAYS_PER_YEAR)
    return float(annual_ret), float(annual_vol), n


def _mdd(nav: pd.Series) -> float:
    running_max = nav.cummax()
    dd = (nav - running_max) / running_max
    return float(dd.min())


def summary(
    nav: pd.Series,
    benchmark: pd.Series | None = None,
    trades: pd.DataFrame | None = None,
    equity: pd.Series | None = None,
) -> dict:
    """equity: 绝对市值序列，用于正确计算 turnover（trades.value 是绝对金额）。"""
    out: dict = {}
    annual_ret, annual_vol, n_days = _annualize(nav)
    mdd = _mdd(nav)
    sharpe = (annual_ret - RISK_FREE) / annual_vol if annual_vol > 0 else 0.0
    calmar = annual_ret / abs(mdd) if mdd < 0 else float("inf")

    out["n_days"] = int(n_days)
    out["years"] = round(n_days / TRADING_DAYS_PER_YEAR, 2)
    out["cum_return"] = float(nav.iloc[-1] / nav.iloc[0] - 1)
    out["annual_return"] = annual_ret
    out["annual_vol"] = annual_vol
    out["sharpe"] = float(sharpe)
    out["mdd"] = mdd
    out["calmar"] = float(calmar) if math.isfinite(calmar) else None

    if trades is not None and not trades.empty:
        # turnover 的分母必须是绝对 equity，不能用归一化 nav
        avg_equity = float(equity.mean()) if equity is not None and len(equity) > 0 else float("nan")
        if avg_equity > 0 and n_days > 0:
            turnover = float(trades["value"].sum()) / avg_equity / (n_days / TRADING_DAYS_PER_YEAR)
        else:
            turnover = 0.0
        out["turnover_annual"] = turnover
        out["n_trades"] = int(len(trades))
        out["total_fee"] = float(trades["fee"].sum())
    else:
        out["turnover_annual"] = 0.0
        out["n_trades"] = 0
        out["total_fee"] = 0.0

    if benchmark is not None and len(benchmark) > 0:
        b = benchmark.reindex(nav.index).ffill()
        b_ret, b_vol, _ = _annualize(b)
        out["benchmark_annual_return"] = b_ret
        out["benchmark_mdd"] = _mdd(b)
        out["excess_annual_return"] = annual_ret - b_ret

    return out


def format_report(m: dict) -> str:
    lines = [
        f"回测期间: {m['years']} 年（{m['n_days']} 交易日）",
        f"累计收益: {m['cum_return']:+.2%}",
        f"年化收益: {m['annual_return']:+.2%}",
        f"年化波动: {m['annual_vol']:.2%}",
        f"Sharpe  : {m['sharpe']:.2f}",
        f"最大回撤: {m['mdd']:.2%}",
        f"Calmar  : {m['calmar']:.2f}" if m['calmar'] is not None else "Calmar  : n/a",
        f"年化换手: {m['turnover_annual']:.2f}x",
        f"交易次数: {m['n_trades']}",
        f"总手续费: {m['total_fee']:,.2f}",
    ]
    if "benchmark_annual_return" in m:
        lines.append(f"基准年化: {m['benchmark_annual_return']:+.2%}")
        lines.append(f"基准回撤: {m['benchmark_mdd']:.2%}")
        lines.append(f"超额年化: {m['excess_annual_return']:+.2%}")
    return "\n".join(lines)
