"""每日增量更新脚本。

用法（建议收盘后 17:00 之后运行）：
    python -m scripts.daily_update

幂等：基于 ingest_progress 表，已拉到今天则无操作。
"""
from __future__ import annotations

import sys

from quant_data.api import db_status
from quant_data.ingest import daily_bars, stock_basic


def main() -> int:
    print("=== [1/3] 更新交易日历（保证覆盖今天） ===")
    n = stock_basic.ingest_trade_cal()
    print(f"  trade_cal: {n} 行（只更新有变动的日）")

    print("=== [2/3] 更新股票基础信息（新股 / ST 变动） ===")
    n = stock_basic.ingest_stock_basic()
    print(f"  stock_basic: {n} 行")

    print("=== [3/3] 增量拉取日线 ===")
    df = daily_bars.ingest_all_stocks()
    total_bars = int(df["daily_bar"].sum()) if "daily_bar" in df.columns else 0
    print(f"  新增 daily_bar 行数: {total_bars}")

    info = db_status()
    print(f"\n数据库大小: {info['size_mb']} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
