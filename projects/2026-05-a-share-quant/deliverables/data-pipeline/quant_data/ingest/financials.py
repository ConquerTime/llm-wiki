"""财务指标（季频）拉取。

关键：fina_indicator 必须记录 ann_date（实际公告日），回测时按 ann_date 过滤，
避免用到"报告期结束但还未公告"的数据（前瞻偏差）。
"""
from __future__ import annotations

import time

import pandas as pd
from tqdm import tqdm

from quant_data.config import CONFIG
from quant_data.sources import tushare_source as ts_src
from quant_data.storage import duckdb_store as store


def ingest_fina_indicator(
    ts_codes: list[str] | None = None, throttle_sec: float = 0.3
) -> pd.DataFrame:
    """拉取财务指标。默认拉 stock_basic 中所有股票。

    按 ts_code 粒度请求，一次取到全时段（季频数据量小，无需按日增量）。
    使用 upsert 覆盖：财报会修正，以最新拉取为准。
    """
    if ts_codes is None:
        codes_df = store.query_df("SELECT ts_code FROM stock_basic ORDER BY ts_code")
        ts_codes = codes_df["ts_code"].tolist()

    summaries = []
    end_date = "99991231"  # 全历史
    for ts_code in tqdm(ts_codes, desc="ingest financials"):
        try:
            df = ts_src.fetch_fina_indicator(ts_code, CONFIG.start_date, end_date)
            # 同一 (ts_code, end_date) 可能有多次公告（财报修订），保留 ann_date 最晚的
            if df is not None and not df.empty and "ann_date" in df.columns:
                df = (
                    df.sort_values("ann_date")
                    .drop_duplicates(subset=["ts_code", "end_date"], keep="last")
                    .reset_index(drop=True)
                )
            with store.connect() as conn:
                rows = store.upsert(conn, "fina_indicator", df, ["ts_code", "end_date"])
            summaries.append({"ts_code": ts_code, "rows": rows})
        except Exception as e:
            summaries.append({"ts_code": ts_code, "error": str(e)})
        time.sleep(throttle_sec)
    return pd.DataFrame(summaries)
