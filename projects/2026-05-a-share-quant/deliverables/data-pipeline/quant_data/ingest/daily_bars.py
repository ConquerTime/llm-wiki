"""日线行情 + 复权因子 + 每日基础指标 的拉取与增量更新。"""
from __future__ import annotations

import time
from datetime import datetime, timedelta

import pandas as pd
from tqdm import tqdm

from quant_data.config import CONFIG
from quant_data.sources import tushare_source as ts_src
from quant_data.storage import duckdb_store as store


def _next_day(yyyymmdd: str) -> str:
    d = datetime.strptime(yyyymmdd, "%Y%m%d") + timedelta(days=1)
    return d.strftime("%Y%m%d")


def _today() -> str:
    return datetime.now().strftime("%Y%m%d")


def _decide_start(conn, table: str, ts_code: str, fallback_start: str) -> str:
    """基于进度表决定增量起点。首次拉 = fallback_start；已有进度 = 已拉最新日 +1。"""
    last = store.get_progress(conn, table, ts_code)
    return _next_day(last) if last else fallback_start


def ingest_one_stock(ts_code: str, start_date: str | None = None, end_date: str | None = None) -> dict:
    """拉取单只股票的日线 + 复权因子 + 每日基础。

    增量逻辑：按进度表决定 start，然后整体拉到 end。
    """
    end_date = end_date or _today()
    fallback_start = start_date or CONFIG.start_date
    summary = {"ts_code": ts_code, "daily_bar": 0, "adj_factor": 0, "daily_basic": 0}

    with store.connect() as conn:
        # daily_bar
        s = _decide_start(conn, "daily_bar", ts_code, fallback_start)
        if s <= end_date:
            df = ts_src.fetch_daily(ts_code, s, end_date)
            summary["daily_bar"] = store.upsert(conn, "daily_bar", df, ["ts_code", "trade_date"])
            if df is not None and not df.empty:
                store.update_progress(conn, "daily_bar", ts_code, df["trade_date"].max())

        # adj_factor
        s = _decide_start(conn, "adj_factor", ts_code, fallback_start)
        if s <= end_date:
            df = ts_src.fetch_adj_factor(ts_code, s, end_date)
            summary["adj_factor"] = store.upsert(conn, "adj_factor", df, ["ts_code", "trade_date"])
            if df is not None and not df.empty:
                store.update_progress(conn, "adj_factor", ts_code, df["trade_date"].max())

        # daily_basic
        s = _decide_start(conn, "daily_basic", ts_code, fallback_start)
        if s <= end_date:
            df = ts_src.fetch_daily_basic(ts_code, s, end_date)
            summary["daily_basic"] = store.upsert(
                conn, "daily_basic", df, ["ts_code", "trade_date"]
            )
            if df is not None and not df.empty:
                store.update_progress(conn, "daily_basic", ts_code, df["trade_date"].max())

    return summary


def ingest_all_stocks(
    start_date: str | None = None,
    end_date: str | None = None,
    throttle_sec: float = 0.3,
) -> pd.DataFrame:
    """遍历 stock_basic 表中所有股票，逐只增量拉取。

    throttle_sec: 每只股票之间的延迟，避免触发 Tushare 频率限制。
    """
    codes_df = store.query_df(
        "SELECT ts_code FROM stock_basic ORDER BY ts_code"
    )
    if codes_df.empty:
        raise RuntimeError("stock_basic 为空，请先运行 ingest_stock_basic()")

    summaries = []
    for ts_code in tqdm(codes_df["ts_code"].tolist(), desc="ingest daily"):
        try:
            s = ingest_one_stock(ts_code, start_date, end_date)
            summaries.append(s)
        except Exception as e:
            summaries.append({"ts_code": ts_code, "error": str(e)})
        time.sleep(throttle_sec)
    return pd.DataFrame(summaries)
