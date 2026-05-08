"""股票基础信息 + 交易日历 的拉取与落库。"""
from __future__ import annotations

from datetime import datetime

from quant_data.config import CONFIG
from quant_data.sources import tushare_source as ts_src
from quant_data.storage import duckdb_store as store


def ingest_stock_basic() -> int:
    """拉取全市场股票基础信息。每次全量覆盖（约 5000 行，成本低）。"""
    df = ts_src.fetch_stock_basic()
    with store.connect() as conn:
        conn.execute("DELETE FROM stock_basic")
        rows = store.upsert(conn, "stock_basic", df, keys=["ts_code"])
    return rows


def ingest_trade_cal(start_date: str | None = None, end_date: str | None = None) -> int:
    """拉取交易日历。"""
    start_date = start_date or CONFIG.start_date
    end_date = end_date or datetime.now().strftime("%Y%m%d")
    df = ts_src.fetch_trade_cal(start_date, end_date)
    with store.connect() as conn:
        rows = store.upsert(conn, "trade_cal", df, keys=["cal_date"])
    return rows
