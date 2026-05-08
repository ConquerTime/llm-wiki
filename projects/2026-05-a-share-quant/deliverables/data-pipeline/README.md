# Quant Data Pipeline

A 股量化数据管道：Tushare Pro + AkShare → DuckDB。

对 M3 回测层提供统一读数 API。

## 决策

详见 [[projects/2026-05-a-share-quant/notes/m2-decisions.md|M2 数据管道决策记录]]。

核心选择：
- **数据源**：Tushare Pro 主，AkShare 补（龙虎榜等延后）
- **存储**：DuckDB（单文件列存 SQL）
- **范围**：2016-01-01 至今，全 A 股 ~5000 只，日频
- **复权**：前复权（qfq），计算链在读数 API 内完成

## 安装

```bash
cd projects/2026-05-a-share-quant/deliverables/data-pipeline

# 用 uv（推荐）
uv venv
source .venv/bin/activate
uv pip install -e .

# 或用 pip
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 配置

1. 注册 Tushare Pro 账号：https://tushare.pro
2. 复制 `.env.example` 为 `.env`，填入 token：
   ```
   TUSHARE_TOKEN=你的_token
   ```
3. 免费 100 积分不足以拉全量日线，建议升级到 2000+（约 200 元/年）。

## 使用

### 首次全量拉数

```bash
# 冒烟测试：只拉 5 只股票（约 1 分钟）
python -m scripts.bootstrap --smoke

# 只拉行情，跳过财务（约 75 分钟）
python -m scripts.bootstrap --skip-financials

# 全量（约 100 分钟）
python -m scripts.bootstrap
```

### 每日增量更新

```bash
# 建议每日 17:00 之后跑（收盘后数据更新）
python -m scripts.daily_update
```

幂等：基于 `ingest_progress` 表，重复运行不会重复拉。

### 读取数据（M3 回测层用）

```python
from quant_data.api import get_bars, get_stock_list, get_trading_dates

# 股票列表（排除 ST、上市满 250 天）
stocks = get_stock_list(exclude_st=True, min_list_days=250)

# 日线（前复权）
bars = get_bars("000001.SZ", start="2024-01-01", end="2024-12-31")

# 交易日序列
dates = get_trading_dates(start="2024-01-01", end="2024-12-31")

# 财务指标（as_of_date 防止前瞻偏差）
from quant_data.api import get_fina_indicator
fina = get_fina_indicator("000001.SZ", as_of_date="2024-06-30")
```

## 数据表

| 表 | 内容 | 主键 |
|---|---|---|
| stock_basic | 股票基础信息 | ts_code |
| trade_cal | 交易日历 | cal_date |
| daily_bar | 日线行情（未复权） | (ts_code, trade_date) |
| adj_factor | 复权因子 | (ts_code, trade_date) |
| daily_basic | 每日基础指标（换手/市值/估值） | (ts_code, trade_date) |
| fina_indicator | 财务指标季频 | (ts_code, end_date) |
| ingest_progress | 拉取进度（内部用）| (table_name, ts_code) |

## 关键设计说明

### 复权处理

原始行情存"未复权"，读数 API 动态算前复权：
```
qfq_price = price * adj_factor / latest_adj_factor
```
好处：原始值不失真；换复权方式无需重刷数据。

### 前瞻偏差防护

财务数据用 `ann_date`（实际公告日）而非 `end_date`（报告期）过滤。
读取时传 `as_of_date`，只返回当时已公告的数据。

### 幂等与增量

- 每张时序表带主键 → `upsert` 做 delete-then-insert
- `ingest_progress` 表记录每只股票拉到哪一天 → `daily_update` 只拉新日

### 错误处理

单只股票失败不中断全量拉数，错误 ts_code 写到 `daily_ingest_errors.csv`。
手动重试：`ingest_one_stock("600000.SH")`。

## 待办（M3 启动前可选）

- [ ] 指数成分股历史（沪深300/中证500/中证1000），用于指数相对排名
- [ ] 行业分类历史快照（用于行业中性化）
- [ ] 北上资金 / 融资融券余额（如果 M4 策略需要）

## 未覆盖（M4+ 再评估）

- 分钟线 / tick（空间大 50x，按需再拉）
- 龙虎榜 / 公告文本（事件驱动策略的输入）
- L2 行情（订单簿，超出本项目范围）
