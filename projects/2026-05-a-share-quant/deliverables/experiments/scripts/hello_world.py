"""M3 Hello-world 回测：茅台 双均线 20/60 交叉。

规则：
- SMA20 上穿 SMA60 → 目标满仓（100%）
- SMA20 下穿或位于 SMA60 下方 → 目标空仓（0%）
- 信号在 t 收盘计算，成交在 t+1 open

用法：
  python -m scripts.hello_world
  python -m scripts.hello_world --ts-code 600519.SH --start 20160101
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                             # experiments/
ENGINE_ROOT = HERE.parent.parent / "data-pipeline"
sys.path.insert(0, str(ENGINE_ROOT))

import pandas as pd  # noqa: E402

from quant_data.api import get_bars  # noqa: E402
from quant_data.backtest import BacktestEngine, buy_and_hold_nav  # noqa: E402
from quant_data.backtest.metrics import summary, format_report  # noqa: E402


def make_sma_cross_strategy(ts_code: str, fast: int, slow: int):
    """返回一个 Strategy 函数：SMA 快慢交叉 → 满仓/空仓。"""
    def strat(asof, bars_hist, portfolio):
        df = bars_hist.get(ts_code)
        if df is None or len(df) < slow:
            return {}  # 数据不足，保持空仓
        close = df["close"]
        sma_f = close.rolling(fast).mean()
        sma_s = close.rolling(slow).mean()
        if pd.isna(sma_f.iloc[-1]) or pd.isna(sma_s.iloc[-1]):
            return {}
        if sma_f.iloc[-1] > sma_s.iloc[-1]:
            return {ts_code: 1.0}
        else:
            return {ts_code: 0.0}
    return strat


def buy_and_hold_strategy(ts_code: str):
    """基准：首日满仓买入后持有。"""
    def strat(asof, bars_hist, portfolio):
        return {ts_code: 1.0}
    return strat


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ts-code", default="600519.SH")
    parser.add_argument("--fast", type=int, default=20)
    parser.add_argument("--slow", type=int, default=60)
    parser.add_argument("--start", default="20160101")
    parser.add_argument("--end", default=None)
    parser.add_argument("--cash", type=float, default=1_000_000.0)
    parser.add_argument("--adj", default="qfq", choices=["qfq", "hfq", "none"],
                        help="策略标的复权方式。ETF/指数需用 none")
    parser.add_argument("--benchmark", default=None,
                        help="基准 ts_code（可跨标的）。未设则用策略同标的 buy&hold")
    parser.add_argument("--benchmark-adj", default="qfq", choices=["qfq", "hfq", "none"])
    parser.add_argument("--out", default=str(ROOT / "data" / "hello_world.json"))
    args = parser.parse_args()

    print(f"[hello-world] 标的 {args.ts_code}，SMA({args.fast})/SMA({args.slow})，"
          f"期间 {args.start} - {args.end or 'latest'}")

    bars_df = get_bars(args.ts_code, start=args.start, end=args.end, adj=args.adj)
    if bars_df.empty:
        print(f"ERROR: {args.ts_code} 无数据", file=sys.stderr)
        return 1
    print(f"  数据 {len(bars_df)} 行，{bars_df['trade_date'].min().date()} ~ "
          f"{bars_df['trade_date'].max().date()}")

    bars = {args.ts_code: bars_df}

    # 主策略
    strat = make_sma_cross_strategy(args.ts_code, args.fast, args.slow)
    res = BacktestEngine(bars, strat, start_cash=args.cash).run()

    # 基准：若指定 --benchmark 则跨标的读；否则同标的 buy&hold
    if args.benchmark:
        bench_df = get_bars(args.benchmark, start=args.start, end=args.end,
                            adj=args.benchmark_adj)
        if bench_df.empty:
            print(f"ERROR: 基准 {args.benchmark} 无数据", file=sys.stderr)
            return 1
        bench_nav = buy_and_hold_nav(bench_df)
        print(f"  基准 {args.benchmark}（跨标的，{args.benchmark_adj}）")
    else:
        bench_res = BacktestEngine(bars, buy_and_hold_strategy(args.ts_code),
                                   start_cash=args.cash).run()
        bench_nav = bench_res.nav
        print(f"  基准 {args.ts_code}（同标的买入持有）")

    m = summary(res.nav, benchmark=bench_nav, trades=res.trades,
                equity=res.daily["equity"])
    print("\n=== 策略: SMA Cross ===")
    print(format_report(m))

    print(f"\n交易次数 {len(res.trades)}，Suspect 日 {len(res.suspect_days)}")
    if not res.suspect_days.empty:
        print("Suspect 日列表（复权跳变，|ret| > 30%）:")
        print(res.suspect_days.to_string(index=False))

    # 导出
    payload = {
        "args": vars(args),
        "metrics": m,
        "n_trades": int(len(res.trades)),
        "first_nav": float(res.nav.iloc[0]),
        "last_nav": float(res.nav.iloc[-1]),
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str),
                              encoding="utf-8")

    # 把 nav 存 csv 方便后续可视化
    out_csv = Path(args.out).with_suffix(".csv")
    pd.DataFrame({
        "date": res.nav.index,
        "nav_strategy": res.nav.values,
        "nav_benchmark": bench_nav.reindex(res.nav.index).ffill().values,
    }).to_csv(out_csv, index=False)
    print(f"\nJSON  -> {args.out}")
    print(f"CSV   -> {out_csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
