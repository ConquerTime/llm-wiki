"""一次性拉取基准：沪深 300 指数 000300.SH + 沪深 300 ETF 510300.SH。

两者都入 daily_bar 表（schema 相容）。
不入 adj_factor（指数无复权；ETF 的分红影响忽略）。
不入 stock_basic（避免污染股票列表）。

用法：
  python -m scripts.ingest_benchmarks
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from quant_data.sources import tushare_source as ts_src  # noqa: E402
from quant_data.storage import duckdb_store as store  # noqa: E402

BENCHMARKS = [
    ("000300.SH", "fetch_index_daily", "沪深 300 指数"),
    ("510300.SH", "fetch_fund_daily",  "华泰柏瑞沪深 300 ETF"),
]

START = "20160101"
END   = "20260508"


def main() -> int:
    for ts_code, fn_name, label in BENCHMARKS:
        print(f"[{ts_code}] {label} via {fn_name}...")
        fn = getattr(ts_src, fn_name)
        df = fn(ts_code, START, END)
        if df is None or df.empty:
            print(f"  WARN: 空返回")
            continue
        print(f"  fetched {len(df)} rows, {df['trade_date'].min()} ~ {df['trade_date'].max()}")
        with store.connect() as conn:
            n = store.upsert(conn, "daily_bar", df, ["ts_code", "trade_date"])
            print(f"  upserted {n} rows into daily_bar")
            # 对 daily_bar 写一条 progress，后续 daily_update 就会增量
            store.update_progress(conn, "daily_bar", ts_code, df["trade_date"].max())
    return 0


if __name__ == "__main__":
    sys.exit(main())
