"""日频 A 股回测引擎 · 最小实现。

设计原则：
- 策略函数只回答"今日收盘后，明日开盘我想持有什么权重" → 时间对齐干净，无未来函数
- 成交在 t+1 的 open 执行（T+1 合规 + 规避当日信号用当日收盘价）
- 前复权数据输入，NAV 用 close 估值
- 停牌日（bar 缺失）：持仓按最近 close 估值，不成交
- M2 体检发现的 4 条防御：
    样本池剔除 → 由调用方传入的 bars 已过滤
    停牌断点 → 本引擎按 bar 缺失日"冻结"
    复权跳变 → 日收益 > 30% 打 WARN 不中断
    财务前瞻 → 本引擎不涉及财务

简化（M4 再补）：
- 不模拟滑点 / 涨跌停拒单
- 不做组合再平衡的税费优化
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable, Protocol

import pandas as pd

logger = logging.getLogger(__name__)

# 手续费（A 股常规）
BUY_FEE = 0.00025   # 0.025% 佣金
SELL_FEE = 0.00125  # 0.125% 佣金 + 印花税

# M2 体检阈值：复权日收益 > 30% 打 WARN
ADJ_SUSPECT_THRESHOLD = 0.30


class Strategy(Protocol):
    """策略协议。
    每个交易日收盘后调用，返回目标权重 dict: {ts_code: weight(0-1)}。
    权重总和不超过 1（超过部分由引擎按比例缩放）。
    """
    def __call__(self, asof: pd.Timestamp, bars_hist: dict[str, pd.DataFrame],
                 portfolio: "Portfolio") -> dict[str, float]:
        ...


@dataclass
class Portfolio:
    """投资组合状态（只在引擎内部变更）。"""
    cash: float
    holdings: dict[str, float] = field(default_factory=dict)  # ts_code -> shares
    last_close: dict[str, float] = field(default_factory=dict)  # ts_code -> last seen close

    def equity(self) -> float:
        """市值 = cash + sum(shares * last_close)。"""
        pos_value = sum(self.holdings.get(c, 0) * self.last_close.get(c, 0)
                        for c in self.holdings)
        return self.cash + pos_value


@dataclass
class BacktestResult:
    nav: pd.Series                 # index=date, value=NAV
    trades: pd.DataFrame           # date, ts_code, side, shares, price, value, fee
    daily: pd.DataFrame            # date, cash, equity, holdings_json
    suspect_days: pd.DataFrame     # 复权跳变记录


def _prepare_bars(bars: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """标准化 bars：trade_date 转 datetime、设为 index、按日期排序。
    期望列：trade_date, open, high, low, close, vol, amount。
    """
    out: dict[str, pd.DataFrame] = {}
    for code, df in bars.items():
        if df is None or df.empty:
            continue
        d = df.copy()
        if not pd.api.types.is_datetime64_any_dtype(d["trade_date"]):
            d["trade_date"] = pd.to_datetime(d["trade_date"])
        d = d.set_index("trade_date").sort_index()
        out[code] = d
    return out


def _union_dates(bars: dict[str, pd.DataFrame]) -> pd.DatetimeIndex:
    idx: pd.DatetimeIndex | None = None
    for df in bars.values():
        if idx is None:
            idx = df.index
        else:
            idx = idx.union(df.index)
    return idx if idx is not None else pd.DatetimeIndex([])


def _check_adj_suspect(bars: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """扫一遍检查日收益 > 30%。只记录，不剔除。"""
    records = []
    for code, df in bars.items():
        if "close" not in df.columns:
            continue
        ret = df["close"].pct_change()
        mask = ret.abs() > ADJ_SUSPECT_THRESHOLD
        if mask.any():
            for date, r in ret[mask].items():
                records.append({"ts_code": code, "date": date, "ret": float(r)})
    return pd.DataFrame(records)


class BacktestEngine:
    def __init__(
        self,
        bars: dict[str, pd.DataFrame],
        strategy: Callable,
        start_cash: float = 1_000_000.0,
        start_date: pd.Timestamp | str | None = None,
        end_date: pd.Timestamp | str | None = None,
        fast_mode: bool = False,
    ):
        """fast_mode=True 时不给 strategy 切片 hist dict（每日仅传原始 bars
        reference），策略自行做 asof 对齐。适合全市场扫描避免 1000 万次切片。"""
        self.bars = _prepare_bars(bars)
        self.strategy = strategy
        self.start_cash = start_cash
        self.fast_mode = fast_mode

        self.dates = _union_dates(self.bars)
        if start_date is not None:
            self.dates = self.dates[self.dates >= pd.Timestamp(start_date)]
        if end_date is not None:
            self.dates = self.dates[self.dates <= pd.Timestamp(end_date)]

        self.portfolio = Portfolio(cash=start_cash)
        self.trades: list[dict] = []
        self.daily: list[dict] = []

        self.suspect_days = _check_adj_suspect(self.bars)
        if not self.suspect_days.empty:
            logger.warning(
                "引擎启动扫描发现 %d 日复权跳变 (ret > %.0f%%)。不中断，仅记录。",
                len(self.suspect_days), ADJ_SUSPECT_THRESHOLD * 100,
            )

    # ---------- 交易原语 ----------

    def _mark_close(self, date: pd.Timestamp) -> None:
        """用当日 close 更新 portfolio.last_close（停牌日保留前值）。"""
        for code, df in self.bars.items():
            if date in df.index:
                self.portfolio.last_close[code] = float(df.at[date, "close"])

    def _execute_orders(
        self, exec_date: pd.Timestamp, target_weights: dict[str, float]
    ) -> None:
        """在 exec_date 的 open 价成交，使组合权重逼近 target_weights。"""
        # 用 exec_date 的 open 作为成交价；若该股无 bar → 跳过（停牌）
        # 价格字典需包含"目标买入"和"当前持仓"两类 code，否则持仓无法卖出退出
        prices: dict[str, float] = {}
        codes_needed = set(target_weights) | set(self.portfolio.holdings)
        for code in codes_needed:
            if code not in self.bars:
                continue
            df = self.bars[code]
            if exec_date not in df.index:
                continue  # 停牌，不交易
            prices[code] = float(df.at[exec_date, "open"])

        # 按 equity 分配目标市值
        equity = self.portfolio.equity()
        # 归一化权重（若 sum > 1 缩放）
        tw = dict(target_weights)
        s = sum(tw.values())
        if s > 1.0:
            tw = {k: v / s for k, v in tw.items()}

        target_value = {code: equity * w for code, w in tw.items()}

        # 先卖（把不在 target 或权重降低的卖掉）
        for code, shares in list(self.portfolio.holdings.items()):
            if shares <= 0:
                continue
            target = target_value.get(code, 0.0)
            px = prices.get(code)
            if px is None:
                continue  # 停牌不卖
            cur_val = shares * px
            if cur_val > target:
                sell_val = cur_val - target
                # 按 100 股整手
                sell_shares = int(sell_val / px / 100) * 100
                if sell_shares <= 0:
                    continue
                if sell_shares > shares:
                    sell_shares = int(shares // 100) * 100
                fee = sell_shares * px * SELL_FEE
                self.portfolio.cash += sell_shares * px - fee
                self.portfolio.holdings[code] = shares - sell_shares
                if self.portfolio.holdings[code] <= 0:
                    del self.portfolio.holdings[code]
                self.trades.append({
                    "date": exec_date, "ts_code": code, "side": "sell",
                    "shares": sell_shares, "price": px,
                    "value": sell_shares * px, "fee": fee,
                })

        # 再买
        for code, target in target_value.items():
            px = prices.get(code)
            if px is None or px <= 0:
                continue
            cur_shares = self.portfolio.holdings.get(code, 0)
            cur_val = cur_shares * px
            if target > cur_val:
                need_val = target - cur_val
                # 留 buy_fee 空间
                avail_cash = self.portfolio.cash
                need_val = min(need_val, avail_cash / (1 + BUY_FEE))
                buy_shares = int(need_val / px / 100) * 100
                if buy_shares <= 0:
                    continue
                cost = buy_shares * px
                fee = cost * BUY_FEE
                if cost + fee > self.portfolio.cash:
                    continue
                self.portfolio.cash -= (cost + fee)
                self.portfolio.holdings[code] = cur_shares + buy_shares
                self.trades.append({
                    "date": exec_date, "ts_code": code, "side": "buy",
                    "shares": buy_shares, "price": px,
                    "value": cost, "fee": fee,
                })

    # ---------- 主循环 ----------

    def run(self) -> BacktestResult:
        if len(self.dates) == 0:
            raise ValueError("no trading dates available for backtest")

        # 每日：mark_close → 记录 equity → 生成信号 → 明日开盘执行
        pending_weights: dict[str, float] | None = None
        for i, date in enumerate(self.dates):
            # 1. 若有昨日信号，今日 open 执行
            if pending_weights is not None:
                self._execute_orders(date, pending_weights)
                pending_weights = None

            # 2. 收盘：更新 last_close
            self._mark_close(date)

            # 3. 记录当日收盘后 NAV
            self.daily.append({
                "date": date,
                "cash": self.portfolio.cash,
                "equity": self.portfolio.equity(),
                "holdings": dict(self.portfolio.holdings),
            })

            # 4. 策略生成明日目标权重
            if i < len(self.dates) - 1:
                if self.fast_mode:
                    # 不切片：策略自己用 asof 做对齐（适合全市场扫描）
                    pending_weights = self.strategy(date, self.bars, self.portfolio)
                else:
                    hist = {code: df.loc[:date] for code, df in self.bars.items()}
                    pending_weights = self.strategy(date, hist, self.portfolio)

        daily_df = pd.DataFrame(self.daily).set_index("date")
        nav = daily_df["equity"] / self.start_cash
        trades_df = pd.DataFrame(self.trades) if self.trades else pd.DataFrame(
            columns=["date", "ts_code", "side", "shares", "price", "value", "fee"]
        )
        return BacktestResult(
            nav=nav,
            trades=trades_df,
            daily=daily_df,
            suspect_days=self.suspect_days,
        )


def run(
    bars: dict[str, pd.DataFrame],
    strategy: Callable,
    start_cash: float = 1_000_000.0,
    start_date: str | None = None,
    end_date: str | None = None,
) -> BacktestResult:
    """便捷入口。"""
    return BacktestEngine(bars, strategy, start_cash, start_date, end_date).run()
