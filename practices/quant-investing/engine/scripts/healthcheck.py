"""M2 数据健康体检：只读，不改库。

检查 7 项：
  1. 股票覆盖（stock_basic 有但 daily_bar 没有的股票）
  2. 交易日覆盖（成交股票数过低的交易日）
  3. 财务季度连续性（上市后缺失的季度）
  4. 停复牌一致性（非交易日的 daily_bar / vol=0 的行）
  5. 复权一致性（adj_factor 非单调、前复权日收益 > ±30%）
  6. 财报修正（同 ts_code + end_date 多条 → 主键已防住，做校验）
  7. 价量异常（负值 / high<low / vol=0 但 amount>0 等）

每项输出：通过 ✓ / 告警 ⚠ / 失败 ✗，附 ≤50 条样本和分布统计。
产出：
  - JSON  : data/healthcheck.json
  - 报告  : notes/m2-data-healthcheck.md（调用方写入，本脚本只打印 markdown）

用法：
  python -m scripts.healthcheck               # 打印到 stdout
  python -m scripts.healthcheck --json-only   # 只写 json
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# 允许 `python scripts/healthcheck.py` 直接跑
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from quant_data.storage.duckdb_store import connect, db_info  # noqa: E402

SAMPLE_LIMIT = 50
ADJ_RETURN_THRESHOLD = 0.30  # 前复权单日收益 > ±30% 视为异常


@dataclass
class CheckResult:
    name: str
    status: str  # "pass" | "warn" | "fail"
    summary: str
    metrics: dict[str, Any] = field(default_factory=dict)
    samples: list[dict] = field(default_factory=list)

    def icon(self) -> str:
        return {"pass": "✓", "warn": "⚠", "fail": "✗"}[self.status]


# ---------- 7 项检查 ----------

def check_stock_coverage(conn) -> CheckResult:
    """stock_basic 里的股票是否都在 daily_bar 出现。"""
    total = conn.execute("SELECT COUNT(*) FROM stock_basic").fetchone()[0]
    missing = conn.execute("""
        SELECT sb.ts_code, sb.name, sb.list_date, sb.list_status, sb.delist_date
        FROM stock_basic sb
        LEFT JOIN (SELECT DISTINCT ts_code FROM daily_bar) d USING (ts_code)
        WHERE d.ts_code IS NULL
        ORDER BY sb.list_date
    """).df()
    n_missing = len(missing)
    status = "pass" if n_missing == 0 else ("warn" if n_missing < total * 0.01 else "fail")
    return CheckResult(
        name="1. 股票覆盖",
        status=status,
        summary=f"stock_basic {total} 只，daily_bar 缺失 {n_missing} 只 ({n_missing/total:.2%})",
        metrics={"stock_basic_total": total, "missing_in_daily_bar": n_missing},
        samples=missing.head(SAMPLE_LIMIT).to_dict("records"),
    )


def check_trade_day_coverage(conn) -> CheckResult:
    """每个交易日成交股票数分布；< 4000 的日子标红。"""
    df = conn.execute("""
        SELECT trade_date, COUNT(DISTINCT ts_code) AS n
        FROM daily_bar
        GROUP BY trade_date
        ORDER BY trade_date
    """).df()
    p = df["n"].describe(percentiles=[0.01, 0.05, 0.5, 0.95]).to_dict()
    low = df[df["n"] < 4000].copy()
    # 需要交叉验证：这些低计数日是否确实是交易日
    low_cal = conn.execute("""
        SELECT cal_date, is_open FROM trade_cal
        WHERE cal_date IN (SELECT trade_date FROM daily_bar GROUP BY trade_date HAVING COUNT(DISTINCT ts_code) < 4000)
    """).df()
    is_open_map = dict(zip(low_cal["cal_date"], low_cal["is_open"]))
    low["is_open"] = low["trade_date"].map(is_open_map)
    # 非早期市场：2016 之后 A 股上市数本就少，看 2020 之后
    recent_low = low[low["trade_date"] >= "20200101"]
    status = "pass" if len(recent_low) == 0 else ("warn" if len(recent_low) < 10 else "fail")
    return CheckResult(
        name="2. 交易日覆盖",
        status=status,
        summary=f"共 {len(df)} 个交易日；< 4000 只成交的日子 {len(low)} 天，其中 2020 后 {len(recent_low)} 天",
        metrics={
            "trade_days": len(df),
            "n_stocks_min": int(p["min"]),
            "n_stocks_p01": int(p["1%"]),
            "n_stocks_p50": int(p["50%"]),
            "n_stocks_max": int(p["max"]),
            "days_below_4000_total": len(low),
            "days_below_4000_since_2020": len(recent_low),
        },
        samples=recent_low.head(SAMPLE_LIMIT).to_dict("records"),
    )


def check_fina_quarter_continuity(conn) -> CheckResult:
    """上市满一年的股票，应按季度连续有 fina_indicator。"""
    # 只看上市 ≥ 1 年、仍在交易的股票，检查是否有季度缺失
    df = conn.execute("""
        WITH eligible AS (
            SELECT ts_code, list_date FROM stock_basic
            WHERE list_status = 'L'
              AND list_date <= strftime(CURRENT_DATE - INTERVAL '1 year', '%Y%m%d')
        ),
        q AS (
            SELECT ts_code,
                   COUNT(DISTINCT end_date) AS n_quarters,
                   MIN(end_date) AS first_q,
                   MAX(end_date) AS last_q
            FROM fina_indicator
            GROUP BY ts_code
        )
        SELECT e.ts_code, e.list_date, q.n_quarters, q.first_q, q.last_q
        FROM eligible e
        LEFT JOIN q USING (ts_code)
        ORDER BY e.ts_code
    """).df()

    no_fina = df[df["n_quarters"].isna()]
    # 期望季度数 = 从上市到现在的季度数，允许 ±2
    df2 = df.dropna(subset=["n_quarters"]).copy()
    df2["expected"] = df2.apply(lambda r: _expected_quarters(r["list_date"]), axis=1)
    df2["gap"] = df2["expected"] - df2["n_quarters"]
    suspicious = df2[df2["gap"] >= 4].sort_values("gap", ascending=False)

    total = len(df)
    n_missing_all = len(no_fina)
    n_gap = len(suspicious)
    status = "pass" if n_gap + n_missing_all < total * 0.02 else ("warn" if n_gap + n_missing_all < total * 0.10 else "fail")
    samples = (
        no_fina.head(SAMPLE_LIMIT // 2).to_dict("records")
        + suspicious.head(SAMPLE_LIMIT // 2).to_dict("records")
    )
    return CheckResult(
        name="3. 财务季度连续性",
        status=status,
        summary=f"上市 ≥1 年的 {total} 只中，{n_missing_all} 只无财报，{n_gap} 只季度缺口 ≥4",
        metrics={
            "eligible_total": total,
            "no_financials": n_missing_all,
            "gap_ge_4_quarters": n_gap,
        },
        samples=samples,
    )


def _expected_quarters(list_date: str) -> int:
    """从上市日期到今天应有的季报数（粗估）。"""
    import datetime as dt
    try:
        d = dt.datetime.strptime(list_date, "%Y%m%d").date()
    except Exception:
        return 0
    today = dt.date.today()
    months = (today.year - d.year) * 12 + (today.month - d.month)
    return max(0, months // 3)


def check_suspend_consistency(conn) -> CheckResult:
    """daily_bar 里成交量为 0 的行（停牌/无成交）。"""
    zero_vol = conn.execute("""
        SELECT ts_code, trade_date, close, vol, amount
        FROM daily_bar
        WHERE vol = 0 OR vol IS NULL
        ORDER BY trade_date DESC
    """).df()
    # 非交易日但 daily_bar 有数据？
    non_trading = conn.execute("""
        SELECT d.trade_date, COUNT(*) AS n
        FROM daily_bar d
        LEFT JOIN trade_cal t ON d.trade_date = t.cal_date
        WHERE t.is_open = 0 OR t.is_open IS NULL
        GROUP BY d.trade_date
    """).df()
    # vol=0 但 amount > 0（自相矛盾）
    inconsistent = conn.execute("""
        SELECT ts_code, trade_date, vol, amount
        FROM daily_bar
        WHERE (vol = 0 OR vol IS NULL) AND amount > 0
    """).df()
    n_zero = len(zero_vol)
    n_non_trading = int(non_trading["n"].sum()) if len(non_trading) else 0
    n_inconsistent = len(inconsistent)
    status = "pass" if n_non_trading == 0 and n_inconsistent == 0 else "warn"
    return CheckResult(
        name="4. 停复牌一致性",
        status=status,
        summary=f"vol=0 行 {n_zero}；非交易日却有数据 {n_non_trading}；vol=0 但 amount>0 {n_inconsistent}",
        metrics={
            "zero_vol_rows": n_zero,
            "non_trading_day_rows": n_non_trading,
            "vol0_amount_positive": n_inconsistent,
        },
        samples=inconsistent.head(SAMPLE_LIMIT).to_dict("records"),
    )


def check_adj_consistency(conn) -> CheckResult:
    """adj_factor 应按 trade_date 单调非减；前复权日收益 > ±30% 标异常。"""
    # 5a: adj_factor 非单调
    non_monotonic = conn.execute("""
        WITH w AS (
            SELECT ts_code, trade_date, adj_factor,
                   LAG(adj_factor) OVER (PARTITION BY ts_code ORDER BY trade_date) AS prev_f
            FROM adj_factor
        )
        SELECT ts_code, trade_date, adj_factor, prev_f
        FROM w WHERE prev_f IS NOT NULL AND adj_factor < prev_f
        ORDER BY trade_date DESC
    """).df()
    n_non_mono = len(non_monotonic)

    # 5b: 前复权单日收益异常
    # close_qfq = close * adj_factor / latest_adj_factor; ratio = close * adj
    extreme = conn.execute(f"""
        WITH j AS (
            SELECT d.ts_code, d.trade_date, d.close, f.adj_factor,
                   d.close * f.adj_factor AS adj_close
            FROM daily_bar d
            JOIN adj_factor f USING (ts_code, trade_date)
            WHERE d.close IS NOT NULL AND d.close > 0 AND f.adj_factor IS NOT NULL
        ),
        w AS (
            SELECT ts_code, trade_date, adj_close,
                   LAG(adj_close) OVER (PARTITION BY ts_code ORDER BY trade_date) AS prev_adj_close
            FROM j
        )
        SELECT ts_code, trade_date, adj_close, prev_adj_close,
               (adj_close - prev_adj_close) / prev_adj_close AS ret
        FROM w
        WHERE prev_adj_close IS NOT NULL AND prev_adj_close > 0
          AND ABS((adj_close - prev_adj_close) / prev_adj_close) > {ADJ_RETURN_THRESHOLD}
        ORDER BY ABS((adj_close - prev_adj_close) / prev_adj_close) DESC
    """).df()
    n_extreme = len(extreme)

    status = "pass" if n_non_mono == 0 and n_extreme == 0 else ("warn" if n_non_mono == 0 and n_extreme < 500 else "fail")
    return CheckResult(
        name="5. 复权一致性",
        status=status,
        summary=(
            f"adj_factor 非单调 {n_non_mono} 行；"
            f"前复权日收益 > ±{ADJ_RETURN_THRESHOLD:.0%} 异常 {n_extreme} 行"
        ),
        metrics={
            "non_monotonic_adj": n_non_mono,
            "extreme_daily_return": n_extreme,
            "threshold": ADJ_RETURN_THRESHOLD,
        },
        samples=extreme.head(SAMPLE_LIMIT).to_dict("records"),
    )


def check_fina_dedup(conn) -> CheckResult:
    """主键 (ts_code, end_date) 已保证唯一，此处双验证。"""
    dup = conn.execute("""
        SELECT ts_code, end_date, COUNT(*) AS n
        FROM fina_indicator
        GROUP BY ts_code, end_date
        HAVING COUNT(*) > 1
    """).df()
    n_dup = len(dup)
    status = "pass" if n_dup == 0 else "fail"
    return CheckResult(
        name="6. 财报去重",
        status=status,
        summary=f"fina_indicator 同 (ts_code, end_date) 重复组数 {n_dup}",
        metrics={"duplicate_groups": n_dup},
        samples=dup.head(SAMPLE_LIMIT).to_dict("records"),
    )


def check_price_sanity(conn) -> CheckResult:
    """价量字段合理性。"""
    neg = conn.execute("""
        SELECT ts_code, trade_date, open, high, low, close, vol, amount
        FROM daily_bar
        WHERE open < 0 OR high < 0 OR low < 0 OR close < 0
           OR vol < 0 OR amount < 0
    """).df()
    hl = conn.execute("""
        SELECT ts_code, trade_date, open, high, low, close
        FROM daily_bar
        WHERE high < low OR close > high OR close < low OR open > high OR open < low
    """).df()
    zero_close = conn.execute("""
        SELECT ts_code, trade_date, close
        FROM daily_bar
        WHERE close = 0 OR close IS NULL
    """).df()
    n_neg, n_hl, n_zero = len(neg), len(hl), len(zero_close)
    status = "pass" if n_neg + n_hl + n_zero == 0 else ("warn" if n_neg + n_hl < 100 else "fail")
    samples = (
        neg.head(SAMPLE_LIMIT // 3).to_dict("records")
        + hl.head(SAMPLE_LIMIT // 3).to_dict("records")
        + zero_close.head(SAMPLE_LIMIT // 3).to_dict("records")
    )
    return CheckResult(
        name="7. 价量合理性",
        status=status,
        summary=f"负值 {n_neg}；high<low 或 OHLC 越界 {n_hl}；close=0/NULL {n_zero}",
        metrics={
            "negative_rows": n_neg,
            "ohlc_inconsistent": n_hl,
            "close_zero_or_null": n_zero,
        },
        samples=samples,
    )


# ---------- 驱动 ----------

CHECKS = [
    check_stock_coverage,
    check_trade_day_coverage,
    check_fina_quarter_continuity,
    check_suspend_consistency,
    check_adj_consistency,
    check_fina_dedup,
    check_price_sanity,
]


def run_all() -> list[CheckResult]:
    results: list[CheckResult] = []
    with connect(read_only=True) as conn:
        for fn in CHECKS:
            print(f"  运行 {fn.__name__} ...", file=sys.stderr)
            results.append(fn(conn))
    return results


def to_markdown(results: list[CheckResult], info: dict) -> str:
    lines = ["# M2 数据健康体检报告", ""]
    lines.append(f"- 数据库：`{info.get('db_path')}`")
    lines.append(f"- 大小：{info.get('size_mb')} MB")
    lines.append("- 表行数：")
    for t, n in (info.get("tables") or {}).items():
        lines.append(f"  - `{t}`: {n:,}")
    lines.append("")
    # 汇总
    counts = {"pass": 0, "warn": 0, "fail": 0}
    for r in results:
        counts[r.status] += 1
    lines.append(f"**结果**：✓ {counts['pass']} / ⚠ {counts['warn']} / ✗ {counts['fail']}")
    lines.append("")
    lines.append("| # | 检查项 | 状态 | 摘要 |")
    lines.append("|---|--------|------|------|")
    for i, r in enumerate(results, 1):
        lines.append(f"| {i} | {r.name} | {r.icon()} | {r.summary} |")
    lines.append("")
    # 详情
    for r in results:
        lines.append(f"## {r.icon()} {r.name}")
        lines.append("")
        lines.append(f"**摘要**：{r.summary}")
        lines.append("")
        if r.metrics:
            lines.append("**指标**：")
            for k, v in r.metrics.items():
                lines.append(f"- `{k}`: {v}")
            lines.append("")
        if r.samples:
            lines.append(f"**样本**（≤{SAMPLE_LIMIT}）：")
            lines.append("")
            lines.append("```")
            for s in r.samples[:SAMPLE_LIMIT]:
                lines.append(json.dumps(s, ensure_ascii=False, default=str))
            lines.append("```")
            lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-only", action="store_true", help="只写 JSON，不打印 markdown")
    parser.add_argument("--out-json", default=str(ROOT / "data" / "healthcheck.json"))
    args = parser.parse_args()

    info = db_info()
    results = run_all()

    # JSON 产出
    payload = {
        "db_info": info,
        "results": [
            {
                "name": r.name,
                "status": r.status,
                "summary": r.summary,
                "metrics": r.metrics,
                "samples": r.samples,
            }
            for r in results
        ],
    }
    Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_json).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    print(f"JSON -> {args.out_json}", file=sys.stderr)

    if not args.json_only:
        print(to_markdown(results, info))
    return 0 if all(r.status != "fail" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
