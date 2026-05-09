"""动量因子。

核心函数 momentum_n：用 long-format 全市场 DataFrame 一次算出全市场、全历史
的 N 日动量，返回索引对齐的 wide DataFrame (index=date, columns=ts_code)。

这样 Spike 里可以 O(1) 取任意 (ts_code, date) 的动量值，避免每日重算。
"""
from __future__ import annotations

import pandas as pd


def momentum_n(bars_long: pd.DataFrame, n: int = 20, price_col: str = "close") -> pd.DataFrame:
    """返回动量矩阵（index=trade_date, columns=ts_code）。

    bars_long 期望列：ts_code, trade_date, close。其他列可以有，会被丢弃。
    """
    if bars_long is None or bars_long.empty:
        return pd.DataFrame()
    # pivot 成 wide 矩阵
    pvt = bars_long.pivot(index="trade_date", columns="ts_code", values=price_col)
    pvt = pvt.sort_index()
    mom = pvt.pct_change(n)
    return mom
