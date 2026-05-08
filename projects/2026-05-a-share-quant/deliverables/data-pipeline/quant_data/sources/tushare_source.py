"""Tushare Pro adapter: 只负责拉数，不碰数据库。"""
from __future__ import annotations

import time
from functools import lru_cache

import pandas as pd
import tushare as ts

from quant_data.config import CONFIG


@lru_cache(maxsize=1)
def _pro_api():
    """延迟初始化 Tushare Pro client。"""
    token = CONFIG.require_token()
    ts.set_token(token)
    return ts.pro_api()


def fetch_stock_basic() -> pd.DataFrame:
    """股票基础信息：代码、名称、上市日、行业、市场、是否 ST。

    返回列：ts_code, symbol, name, area, industry, market, list_date, list_status
    """
    pro = _pro_api()
    fields = "ts_code,symbol,name,area,industry,market,list_date,list_status,delist_date"
    # 合并上市中 L / 已退市 D / 暂停 P
    frames = []
    for status in ("L", "D", "P"):
        df = pro.stock_basic(exchange="", list_status=status, fields=fields)
        frames.append(df)
        time.sleep(0.2)
    return pd.concat(frames, ignore_index=True)


def fetch_trade_cal(start_date: str, end_date: str) -> pd.DataFrame:
    """交易日历。返回列：cal_date(YYYYMMDD), is_open(0/1)。"""
    pro = _pro_api()
    df = pro.trade_cal(exchange="SSE", start_date=start_date, end_date=end_date)
    return df[["cal_date", "is_open"]].copy()


def fetch_daily(ts_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    """单只股票日线（未复权）。

    返回列：ts_code, trade_date, open, high, low, close, pre_close, change,
           pct_chg, vol, amount
    """
    pro = _pro_api()
    df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    return df


def fetch_adj_factor(ts_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    """复权因子。返回列：ts_code, trade_date, adj_factor。"""
    pro = _pro_api()
    df = pro.adj_factor(ts_code=ts_code, start_date=start_date, end_date=end_date)
    return df


def fetch_daily_basic(ts_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    """每日基础指标：换手率、量比、市盈、市净、市销、总市值、流通市值等。"""
    pro = _pro_api()
    df = pro.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date)
    return df


def fetch_fina_indicator(ts_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    """财务指标季频：ROE、毛利率、净利率、资产负债率、营收同比等。"""
    pro = _pro_api()
    df = pro.fina_indicator(ts_code=ts_code, start_date=start_date, end_date=end_date)
    return df
