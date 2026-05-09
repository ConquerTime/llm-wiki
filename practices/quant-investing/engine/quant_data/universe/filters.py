"""样本池负过滤。

目标：给定 asof 日期，返回当日合格的 ts_code 列表。规则见
notes/m4-spike-spec.md §2.2。所有规则都只用现有数据（stock_basic + daily_bar + trade_cal）。

性能考虑：
- build_universe() 一次性拉全量静态信息（stock_basic、交易日历）
- negative_filter_asof(df_static, asof_date) 逐日快速过滤
- 跨日重用静态信息，减少重复查询
"""
from __future__ import annotations

import pandas as pd

from quant_data.storage import duckdb_store as store

# M2 体检 §3 "活跃但无日线" 的 11 只 + 2 只 errors。已在本轮数据修补中补回，
# 但保留黑名单作为安全网，下一轮 bootstrap 若再缺失可以立刻剔除。
BLACKLIST: set[str] = set()

# 明确排除北交所（M2 体检 §5 adj_factor quirk）
EXCLUDE_MARKETS = {"BJ"}


def build_universe(start_date: str = "20160101") -> dict:
    """一次性加载静态信息，后续逐日过滤复用。

    关键：交易日历拉**全历史**（不受 start_date 限制），这样 list_date
    在 start_date 之前的股票才能正确计算 "上市以来已满 N 个交易日"。
    """
    sb = store.query_df("SELECT ts_code, name, list_date, list_status FROM stock_basic")
    sb = sb[sb["list_status"] == "L"].copy()
    sb["market"] = sb["ts_code"].str[-2:]
    sb = sb[~sb["market"].isin(EXCLUDE_MARKETS)]
    sb = sb[~sb["ts_code"].isin(BLACKLIST)]
    sb["is_st"] = sb["name"].str.contains("ST", na=False)
    # 全历史交易日历（ts_code 都是 1990+ 上市）
    cal = store.query_df(
        "SELECT cal_date FROM trade_cal WHERE is_open = 1 ORDER BY cal_date",
    )
    trade_dates = pd.to_datetime(cal["cal_date"])
    cal_array = cal["cal_date"].values
    list_trade_idx: dict[str, int] = {}
    for _, row in sb.iterrows():
        ld = row["list_date"]
        idx = cal_array.searchsorted(ld, side="left")
        list_trade_idx[row["ts_code"]] = int(idx)
    return {
        "stock_static": sb.reset_index(drop=True),
        "trade_dates": trade_dates,
        "cal_array": cal_array,
        "list_trade_idx": list_trade_idx,
    }


def negative_filter_asof(
    ctx: dict,
    asof: str | pd.Timestamp,
    bars_today: pd.DataFrame | None = None,
    min_list_days: int = 250,
    amount_bottom_pct: float = 0.20,
    exclude_st: bool = True,
) -> list[str]:
    """返回 asof 日合格的 ts_code 列表。

    参数：
      ctx: build_universe 返回值
      asof: 当日日期 (YYYYMMDD 或 Timestamp)
      bars_today: 当日全市场 daily_bar（包含 ts_code, amount 列），用于停牌 + 流动性过滤
      min_list_days: 上市不足该日历日数剔除（默认 250 ≈ 1 年）
      amount_bottom_pct: 成交金额末 X% 剔除（默认 20%）

    注：min_list_days 按"日历日"计算（asof - list_date），
    不是交易日。因为 trade_cal 只覆盖 2016+，对早期上市股票无法用交易日 idx。
    """
    if isinstance(asof, pd.Timestamp):
        asof_ts = asof
        asof_str = asof.strftime("%Y%m%d")
    else:
        asof_str = str(asof).replace("-", "")
        asof_ts = pd.Timestamp(asof_str)

    sb = ctx["stock_static"]

    # 1. 上市日过滤（按日历日）
    candidates = sb.copy()
    if min_list_days > 0:
        list_dt = pd.to_datetime(candidates["list_date"], format="%Y%m%d")
        candidates = candidates[(asof_ts - list_dt).dt.days >= min_list_days]

    # 2. ST
    if exclude_st:
        candidates = candidates[~candidates["is_st"]]

    codes = set(candidates["ts_code"])

    # 3/4. 停牌 + 成交额末 20%
    if bars_today is not None and not bars_today.empty:
        bt = bars_today[bars_today["ts_code"].isin(codes)].copy()
        if amount_bottom_pct > 0 and len(bt) > 0:
            threshold = bt["amount"].quantile(amount_bottom_pct)
            bt = bt[bt["amount"] >= threshold]
        codes = set(bt["ts_code"])
    else:
        # 没有 bars 信息 → 无法判停牌/流动性，保守全放
        pass

    return sorted(codes)


def load_all_bars(start_date: str, end_date: str | None = None) -> pd.DataFrame:
    """一次性加载全市场 daily_bar。返回 long-format DataFrame。

    用于 M4 Spike：5800 股 × 2500 日 ≈ 1000 万行。DuckDB 一次 SQL ~3 秒。
    """
    where = ["trade_date >= ?"]
    params: list = [start_date]
    if end_date:
        where.append("trade_date <= ?")
        params.append(end_date)
    sql = f"""
    SELECT b.ts_code, b.trade_date, b.open, b.high, b.low, b.close,
           b.vol, b.amount
    FROM daily_bar b
    WHERE {" AND ".join(where)}
    ORDER BY b.ts_code, b.trade_date
    """
    df = store.query_df(sql, params)
    if not df.empty:
        df["trade_date"] = pd.to_datetime(df["trade_date"])
    return df
