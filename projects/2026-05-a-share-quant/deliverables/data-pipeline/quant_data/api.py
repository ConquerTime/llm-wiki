"""对外统一读数 API。M3 回测层只依赖本模块，不触达 storage/sources。

设计原则：
- 所有返回 pandas.DataFrame，日期列统一为 datetime64[ns]
- 默认前复权（qfq），通过参数切换
- 不做因子计算，只做原始/复权后的干净数据
"""
from __future__ import annotations

import pandas as pd

from quant_data.storage import duckdb_store as store

AdjType = str  # "qfq" | "hfq" | "none"


def get_stock_list(
    only_active: bool = True,
    exclude_st: bool = False,
    min_list_days: int | None = None,
) -> pd.DataFrame:
    """股票列表。

    only_active: 仅上市中（list_status = 'L'）
    exclude_st: 排除 ST（按 name 含 ST 或 *ST 判断；更精准需要另起一张 ST 历史表）
    min_list_days: 过滤上市不足 N 天的次新股
    """
    where = []
    if only_active:
        where.append("list_status = 'L'")
    if exclude_st:
        where.append("name NOT LIKE '%ST%'")
    if min_list_days is not None:
        where.append(
            f"strptime(list_date, '%Y%m%d') <= CURRENT_DATE - INTERVAL '{min_list_days}' DAY"
        )
    sql = "SELECT * FROM stock_basic"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY ts_code"
    return store.query_df(sql)


def get_trading_dates(start: str | None = None, end: str | None = None) -> pd.Series:
    """交易日序列（is_open = 1）。参数 YYYYMMDD 或 YYYY-MM-DD。"""
    where = ["is_open = 1"]
    params: list = []
    if start:
        where.append("cal_date >= ?")
        params.append(start.replace("-", ""))
    if end:
        where.append("cal_date <= ?")
        params.append(end.replace("-", ""))
    sql = "SELECT cal_date FROM trade_cal WHERE " + " AND ".join(where) + " ORDER BY cal_date"
    df = store.query_df(sql, params)
    return pd.to_datetime(df["cal_date"])


def get_bars(
    ts_code: str | list[str],
    start: str | None = None,
    end: str | None = None,
    adj: AdjType = "qfq",
    fields: list[str] | None = None,
) -> pd.DataFrame:
    """获取日线行情。

    adj:
      - "qfq" 前复权（推荐，M3 信号层用）
      - "hfq" 后复权（计算长期收益率用）
      - "none" 原始未复权（需要精确还原历史真实价格时）

    复权逻辑：以最新 adj_factor 为基准做前复权。
      qfq_price = price * adj_factor / latest_adj_factor
      hfq_price = price * adj_factor
    """
    codes = [ts_code] if isinstance(ts_code, str) else list(ts_code)
    codes_sql = ",".join([f"'{c}'" for c in codes])
    where = [f"b.ts_code IN ({codes_sql})"]
    params: list = []
    if start:
        where.append("b.trade_date >= ?")
        params.append(start.replace("-", ""))
    if end:
        where.append("b.trade_date <= ?")
        params.append(end.replace("-", ""))

    if adj == "none":
        sql = f"""
        SELECT b.ts_code, b.trade_date, b.open, b.high, b.low, b.close,
               b.pre_close, b.pct_chg, b.vol, b.amount
        FROM daily_bar b
        WHERE {" AND ".join(where)}
        ORDER BY b.ts_code, b.trade_date
        """
    else:
        # 使用 latest adj_factor per ts_code 做前复权基准
        if adj == "qfq":
            # qfq: price * factor / latest_factor
            adj_expr = "f.adj_factor / lf.latest_factor"
        elif adj == "hfq":
            adj_expr = "f.adj_factor"
        else:
            raise ValueError(f"unknown adj: {adj}")

        sql = f"""
        WITH latest AS (
            SELECT ts_code, MAX(adj_factor) AS latest_factor
            FROM adj_factor
            GROUP BY ts_code
        )
        SELECT
            b.ts_code,
            b.trade_date,
            b.open  * ({adj_expr}) AS open,
            b.high  * ({adj_expr}) AS high,
            b.low   * ({adj_expr}) AS low,
            b.close * ({adj_expr}) AS close,
            b.pre_close * ({adj_expr}) AS pre_close,
            b.pct_chg,
            b.vol,
            b.amount
        FROM daily_bar b
        JOIN adj_factor f ON b.ts_code = f.ts_code AND b.trade_date = f.trade_date
        JOIN latest lf ON b.ts_code = lf.ts_code
        WHERE {" AND ".join(where)}
        ORDER BY b.ts_code, b.trade_date
        """

    df = store.query_df(sql, params)
    if not df.empty:
        df["trade_date"] = pd.to_datetime(df["trade_date"])
        if fields is not None:
            keep = ["ts_code", "trade_date"] + [c for c in fields if c in df.columns]
            df = df[keep]
    return df


def get_daily_basic(
    ts_code: str | list[str],
    start: str | None = None,
    end: str | None = None,
    fields: list[str] | None = None,
) -> pd.DataFrame:
    """每日基础指标（换手率、市值、估值）。"""
    codes = [ts_code] if isinstance(ts_code, str) else list(ts_code)
    codes_sql = ",".join([f"'{c}'" for c in codes])
    where = [f"ts_code IN ({codes_sql})"]
    params: list = []
    if start:
        where.append("trade_date >= ?")
        params.append(start.replace("-", ""))
    if end:
        where.append("trade_date <= ?")
        params.append(end.replace("-", ""))
    sql = (
        "SELECT * FROM daily_basic WHERE "
        + " AND ".join(where)
        + " ORDER BY ts_code, trade_date"
    )
    df = store.query_df(sql, params)
    if not df.empty:
        df["trade_date"] = pd.to_datetime(df["trade_date"])
        if fields is not None:
            keep = ["ts_code", "trade_date"] + [c for c in fields if c in df.columns]
            df = df[keep]
    return df


def get_fina_indicator(
    ts_code: str | list[str],
    as_of_date: str | None = None,
) -> pd.DataFrame:
    """财务指标。关键：as_of_date 过滤 ann_date <= as_of_date，避免前瞻偏差。"""
    codes = [ts_code] if isinstance(ts_code, str) else list(ts_code)
    codes_sql = ",".join([f"'{c}'" for c in codes])
    where = [f"ts_code IN ({codes_sql})"]
    params: list = []
    if as_of_date:
        where.append("ann_date <= ?")
        params.append(as_of_date.replace("-", ""))
    sql = f"""
    SELECT * FROM fina_indicator
    WHERE {" AND ".join(where)}
    ORDER BY ts_code, end_date
    """
    df = store.query_df(sql, params)
    return df


def db_status() -> dict:
    """数据库状态，用于 sanity check。"""
    return store.db_info()
