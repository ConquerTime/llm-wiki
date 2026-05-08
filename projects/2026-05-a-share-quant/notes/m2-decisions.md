# M2 · 数据管道决策记录（ADR）

> 2026-05-08 对齐。下列决策是 M2 的锚点，变更需在 log.md 记录原因。

## 决策 1：数据源 = Tushare Pro 主 + AkShare 补

**选项对比**
- Tushare Pro 主 + AkShare 补 ✅
- AkShare + Baostock 纯免费
- 纯 AkShare

**选择理由**
- Tushare Pro API 规范、字段全、数据稳定性好，财务数据能对上 Wind 口径
- AkShare 免费但接口偶发变动，作为补充源（龙虎榜、北上资金、事件数据）
- 有限付费（~200 元/年）换工程量砍半，经济

**依赖**
- 用户需自行注册 Tushare Pro 账号并充值积分
- token 从环境变量 `TUSHARE_TOKEN` 读取，不入库

## 决策 2：存储 = DuckDB

**选项对比**
- DuckDB ✅
- Parquet 分区
- SQLite

**选择理由**
- 5000 只 × 10 年日线 ≈ 1300 万行，DuckDB 秒级聚合
- 单文件好备份、好分发，无需服务进程
- SQL 原生支持窗口函数，写因子逻辑直观
- `duckdb.sql(...).df()` 即得 pandas DataFrame，与回测框架天然衔接

**数据库文件位置**
- `deliverables/data-pipeline/data/quant.duckdb`（gitignore）

## 决策 3：数据范围

| 维度 | 决策 |
|------|------|
| 时间跨度 | 2016-01-01 至今（约 10 年，覆盖 2 轮牛熊 + 2 次风格切换）|
| 股票池 | 全 A 股 ~5000 只（含已退市/已 ST），回测时按需过滤 |
| 频率 | 日线为主；分钟线延后到 M4 策略需要时再拉 |
| 财务 | 季频，利润表/资产负债表/现金流表主要字段 + 财务指标 |
| 事件数据 | M3 跑通基础回测后再接（龙虎榜、公告、指数成分变更）|

## 决策 4：运行环境 = Python 3.11 + uv

**选项对比**
- Python 3.11 + uv/pip ✅
- Python + conda
- R / Julia

**选择理由**
- 主流量化栈：Tushare / AkShare / DuckDB / pandas / numpy 全部支持
- uv 装包快（Rust 实现），pyproject.toml 声明依赖、lock 版本

## 决策 5：复权方式 = 前复权（qfq）

A 股两种复权：
- **前复权**：历史价按最新价倒推调整 —— 适合**回测与当前对齐**
- **后复权**：未来除权时旧价不变 —— 适合**收益率序列**

**选择前复权**：策略信号（均线、突破）用人类看得懂的近似真实价格，入场价格直接可比。收益率计算用复权后价格做差分，两种复权结果等价。

## 决策 6：模块边界

```
deliverables/data-pipeline/
├── quant_data/            # Python 包
│   ├── __init__.py
│   ├── config.py          # 配置（数据库路径、日期范围、token 读取）
│   ├── sources/           # 数据源 adapter
│   │   ├── __init__.py
│   │   ├── tushare_source.py
│   │   └── akshare_source.py
│   ├── storage/           # DuckDB schema + 写入/读取
│   │   ├── __init__.py
│   │   └── duckdb_store.py
│   ├── ingest/            # 拉取 + 写入流程
│   │   ├── __init__.py
│   │   ├── stock_basic.py   # 股票基础信息（上市日、行业、是否 ST）
│   │   ├── daily_bars.py    # 日线行情
│   │   ├── adj_factor.py    # 复权因子
│   │   └── financials.py    # 财务数据
│   └── api.py             # 对外统一读数 API（get_bars / get_stock_list 等）
├── scripts/
│   ├── bootstrap.py       # 首次全量拉数
│   └── daily_update.py    # 每日增量更新
├── data/                  # DuckDB 文件（gitignore）
├── pyproject.toml
└── README.md
```

**边界原则**
- `sources/` 只负责**从外部拉**，不碰数据库
- `storage/` 只负责**DuckDB schema + 读写**，不碰网络
- `ingest/` 编排两者，处理增量、幂等、复权
- `api.py` 只读、对 M3 回测层稳定输出

## 开放问题（不在 M2 解决）

- 分钟线/tick 是否接入 —— 到 M4 策略若需要日内信号再评估
- 融资融券数据 —— 到 M4 若做对冲再评估
- 舆情 / NLP 公告解析 —— M5+ 话题
- 定时调度（cron / Airflow） —— 本项目 `daily_update.py` 手动跑即可，不引入调度框架
