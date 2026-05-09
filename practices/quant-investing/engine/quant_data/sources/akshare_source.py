"""AkShare adapter: Tushare 不覆盖的补充数据源。

M2 首版先留空（仅声明接口），等到需要龙虎榜/北上资金/公告事件时再填充。
"""
from __future__ import annotations

import pandas as pd


def fetch_lhb(trade_date: str) -> pd.DataFrame:
    """龙虎榜每日明细。占位，M4 事件过滤器阶段实现。"""
    raise NotImplementedError("龙虎榜抓取在 M4 事件过滤器阶段实现")


def fetch_north_flow(start_date: str, end_date: str) -> pd.DataFrame:
    """北上资金流。占位。"""
    raise NotImplementedError("北上资金抓取延后")
