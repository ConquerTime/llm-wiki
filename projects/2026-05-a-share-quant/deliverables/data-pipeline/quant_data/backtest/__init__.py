"""回测引擎：规则驱动的日频 A 股回测。

入口：
  from quant_data.backtest import BacktestEngine, run
"""
from quant_data.backtest.engine import BacktestEngine, BacktestResult, run
from quant_data.backtest.metrics import summary, buy_and_hold_nav

__all__ = ["BacktestEngine", "BacktestResult", "run", "summary", "buy_and_hold_nav"]
