"""DuckDB 存储层：schema 定义 + 幂等写入 + 统一读取。

设计原则：
- 主键用 (ts_code, trade_date) 保证幂等，重复拉数不会产生重复行
- 写入用 INSERT OR REPLACE 语义（DuckDB 的 INSERT ... ON CONFLICT）
- 读取统一走 DataFrame，不暴露 Connection 细节
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

import duckdb
import pandas as pd

from quant_data.config import CONFIG, ensure_data_dir

# DuckDB schema
DDL_STATEMENTS: list[str] = [
    # 股票基础信息
    """
    CREATE TABLE IF NOT EXISTS stock_basic (
        ts_code      VARCHAR PRIMARY KEY,
        symbol       VARCHAR,
        name         VARCHAR,
        area         VARCHAR,
        industry     VARCHAR,
        market       VARCHAR,
        list_date    VARCHAR,  -- YYYYMMDD
        list_status  VARCHAR,  -- L/D/P
        delist_date  VARCHAR
    )
    """,
    # 交易日历
    """
    CREATE TABLE IF NOT EXISTS trade_cal (
        cal_date VARCHAR PRIMARY KEY,  -- YYYYMMDD
        is_open  INTEGER                -- 0/1
    )
    """,
    # 日线行情（未复权原始值）
    """
    CREATE TABLE IF NOT EXISTS daily_bar (
        ts_code    VARCHAR,
        trade_date VARCHAR,  -- YYYYMMDD
        open       DOUBLE,
        high       DOUBLE,
        low        DOUBLE,
        close      DOUBLE,
        pre_close  DOUBLE,
        change     DOUBLE,
        pct_chg    DOUBLE,
        vol        DOUBLE,   -- 成交量（手）
        amount     DOUBLE,   -- 成交额（千元）
        PRIMARY KEY (ts_code, trade_date)
    )
    """,
    # 复权因子
    """
    CREATE TABLE IF NOT EXISTS adj_factor (
        ts_code    VARCHAR,
        trade_date VARCHAR,
        adj_factor DOUBLE,
        PRIMARY KEY (ts_code, trade_date)
    )
    """,
    # 每日基础指标（换手率、市值、估值）
    """
    CREATE TABLE IF NOT EXISTS daily_basic (
        ts_code        VARCHAR,
        trade_date     VARCHAR,
        turnover_rate  DOUBLE,
        turnover_rate_f DOUBLE,
        volume_ratio  DOUBLE,
        pe            DOUBLE,
        pe_ttm        DOUBLE,
        pb            DOUBLE,
        ps            DOUBLE,
        ps_ttm        DOUBLE,
        total_share   DOUBLE,
        float_share   DOUBLE,
        free_share    DOUBLE,
        total_mv      DOUBLE,
        circ_mv       DOUBLE,
        PRIMARY KEY (ts_code, trade_date)
    )
    """,
    # 财务指标（季频，end_date 为报告期）
    """
    CREATE TABLE IF NOT EXISTS fina_indicator (
        ts_code       VARCHAR,
        ann_date      VARCHAR,  -- 实际公告日（关键！避免前瞻）
        end_date      VARCHAR,  -- 报告期
        roe           DOUBLE,
        roe_dt        DOUBLE,
        roa           DOUBLE,
        netprofit_margin DOUBLE,
        grossprofit_margin DOUBLE,
        debt_to_assets DOUBLE,
        current_ratio DOUBLE,
        revenue_yoy   DOUBLE,
        netprofit_yoy DOUBLE,
        PRIMARY KEY (ts_code, end_date)
    )
    """,
    # 拉取进度追踪：每张表每只股票已拉到哪一天
    """
    CREATE TABLE IF NOT EXISTS ingest_progress (
        table_name VARCHAR,
        ts_code    VARCHAR,
        last_date  VARCHAR,  -- YYYYMMDD, 该股票已覆盖的最新交易日
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (table_name, ts_code)
    )
    """,
]


@contextmanager
def connect(read_only: bool = False):
    """DuckDB 连接上下文。首次使用时自动建表。"""
    ensure_data_dir()
    conn = duckdb.connect(str(CONFIG.db_path), read_only=read_only)
    try:
        if not read_only:
            for ddl in DDL_STATEMENTS:
                conn.execute(ddl)
        yield conn
    finally:
        conn.close()


def upsert(conn: duckdb.DuckDBPyConnection, table: str, df: pd.DataFrame, keys: list[str]) -> int:
    """幂等写入：先按主键删除已有行，再 INSERT。

    DuckDB 目前 (1.1) 对 ON CONFLICT 的支持有限，采用 delete-then-insert 模式。
    返回实际写入的行数。
    """
    if df is None or df.empty:
        return 0

    # 只保留 schema 中存在的列
    cols_in_db = [r[0] for r in conn.execute(f"DESCRIBE {table}").fetchall()]
    df = df[[c for c in df.columns if c in cols_in_db]].copy()

    conn.register("__tmp_df", df)
    # 删除冲突行
    where_clauses = " AND ".join([f"{table}.{k} = __tmp_df.{k}" for k in keys])
    conn.execute(
        f"DELETE FROM {table} USING __tmp_df WHERE {where_clauses}"
    )
    # 插入
    col_list = ",".join(df.columns)
    conn.execute(f"INSERT INTO {table} ({col_list}) SELECT {col_list} FROM __tmp_df")
    conn.unregister("__tmp_df")
    return len(df)


def get_progress(conn: duckdb.DuckDBPyConnection, table: str, ts_code: str) -> str | None:
    """查询某张表、某只股票的已覆盖最新交易日。"""
    row = conn.execute(
        "SELECT last_date FROM ingest_progress WHERE table_name = ? AND ts_code = ?",
        [table, ts_code],
    ).fetchone()
    return row[0] if row else None


def update_progress(
    conn: duckdb.DuckDBPyConnection, table: str, ts_code: str, last_date: str
) -> None:
    conn.execute(
        """
        INSERT INTO ingest_progress (table_name, ts_code, last_date, updated_at)
        VALUES (?, ?, ?, now())
        ON CONFLICT (table_name, ts_code) DO UPDATE SET
            last_date = EXCLUDED.last_date,
            updated_at = now()
        """,
        [table, ts_code, last_date],
    )


def query_df(sql: str, params: list | None = None) -> pd.DataFrame:
    """只读查询，返回 DataFrame。"""
    with connect(read_only=True) as conn:
        if params:
            return conn.execute(sql, params).df()
        return conn.execute(sql).df()


def db_info() -> dict:
    """返回数据库基本信息：表行数、文件大小。"""
    info: dict = {"db_path": str(CONFIG.db_path)}
    p = Path(CONFIG.db_path)
    info["size_mb"] = round(p.stat().st_size / 1024 / 1024, 2) if p.exists() else 0
    if not p.exists():
        return info
    with connect(read_only=True) as conn:
        tables = [
            r[0]
            for r in conn.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema='main'"
            ).fetchall()
        ]
        info["tables"] = {
            t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tables
        }
    return info
