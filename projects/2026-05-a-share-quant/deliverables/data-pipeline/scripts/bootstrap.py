"""首次全量拉数脚本。

用法：
    python -m scripts.bootstrap
    python -m scripts.bootstrap --skip-financials   # 只拉行情，跳过财务
    python -m scripts.bootstrap --smoke             # 只拉 5 只股票用于冒烟测试

预计耗时（throttle 0.3s）：5000 只 × 3 表 × 0.3s ≈ 75 分钟（日线 + 复权 + 每日基础）。
财务数据 5000 只 × 0.3s ≈ 25 分钟。
"""
from __future__ import annotations

import argparse
import sys

from quant_data.api import db_status
from quant_data.ingest import daily_bars, financials, stock_basic


def main() -> int:
    parser = argparse.ArgumentParser(description="首次全量拉数")
    parser.add_argument("--skip-financials", action="store_true", help="跳过财务数据")
    parser.add_argument("--smoke", action="store_true", help="冒烟测试：仅拉 5 只股票")
    args = parser.parse_args()

    print("=== [1/4] 股票基础信息 ===")
    n = stock_basic.ingest_stock_basic()
    print(f"  stock_basic: {n} 行")

    print("=== [2/4] 交易日历 ===")
    n = stock_basic.ingest_trade_cal()
    print(f"  trade_cal: {n} 行")

    print("=== [3/4] 日线 + 复权 + 每日基础 ===")
    if args.smoke:
        # 冒烟：挑 5 只代表性股票
        codes = ["000001.SZ", "600000.SH", "000651.SZ", "600519.SH", "300750.SZ"]
        for c in codes:
            summary = daily_bars.ingest_one_stock(c)
            print(f"  {summary}")
    else:
        df = daily_bars.ingest_all_stocks()
        print(f"  完成 {len(df)} 只股票")
        err = df[df.get("error").notna()] if "error" in df.columns else None
        if err is not None and not err.empty:
            print(f"  [WARN] {len(err)} 只股票失败，详见 daily_ingest_errors.csv")
            err.to_csv("daily_ingest_errors.csv", index=False)

    print("=== [4/4] 财务指标 ===")
    if args.skip_financials:
        print("  已跳过")
    elif args.smoke:
        df = financials.ingest_fina_indicator(
            ["000001.SZ", "600000.SH", "000651.SZ", "600519.SH", "300750.SZ"]
        )
        print(f"  smoke: {df.to_dict('records')}")
    else:
        df = financials.ingest_fina_indicator()
        print(f"  完成 {len(df)} 只股票")

    print("\n=== 数据库状态 ===")
    info = db_status()
    print(f"  路径: {info['db_path']}")
    print(f"  大小: {info['size_mb']} MB")
    for t, cnt in info.get("tables", {}).items():
        print(f"  {t:20s} {cnt:>12,} 行")
    return 0


if __name__ == "__main__":
    sys.exit(main())
