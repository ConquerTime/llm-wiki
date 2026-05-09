---
title: Tushare Pro
type: entity
subtype: product
tags: [tool, business]
created: 2026-05-09
updated: 2026-05-09
sources:
  - "[[projects/2026-05-a-share-quant/retro.md|2026-05 a-share-quant 项目复盘]]"
  - "[[projects/2026-05-a-share-quant/notes/m2-decisions.md|M2 数据管道决策]]"
  - "[[projects/2026-05-a-share-quant/notes/m2-data-healthcheck.md|M2 数据体检]]"
---

# Tushare Pro

> 中文 A 股金融数据接口，按积分分级订阅。a-share-quant 项目的主数据源。

## 基本事实

- **官网**：https://tushare.pro
- **语言**：Python SDK（`pip install tushare`）
- **类型**：付费数据 API，按积分分级
- **覆盖**：A 股 / 港股 / 美股 / 期货 / 期权 / 宏观 / 公告等
- **定价**：免费 100 积分（有限接口）→ 120 元 ≈ 2000 积分 → 更高档位解锁分钟线 / L2
- **替代**：AkShare（免费但接口不稳定）/ Baostock / 米筐（付费绑平台）

## 核心接口（A 股日频）

a-share-quant 项目实际用到的 7 个：

| 接口 | 用途 | 积分要求 |
|---|---|---|
| `stock_basic` | 股票列表 + 上市日 + 行业 | 100 |
| `trade_cal` | 交易日历 | 100 |
| `daily` | 日线 OHLCV | 2000 |
| `adj_factor` | 复权因子 | 2000 |
| `daily_basic` | 换手率 / 市值 / 估值 | 2000 |
| `fina_indicator` | 季度财务指标（ROE / 毛利率等）| 2000 |
| `index_daily` / `fund_daily` | 指数 / ETF 日线 | 2000 |

## 项目内遇到的坑

来自 [[projects/2026-05-a-share-quant/notes/m2-data-healthcheck.md|M2 体检]]：

- **fina_indicator 同季度多公告**：同 (ts_code, end_date) 返回多行（修正公告），入库前需按 ann_date 去重保留最新
- **fina_indicator 覆盖稀**：2000 积分档对**早年上市老股**覆盖不完整（2506/5384 活跃股无财报）。非 tushare bug，是积分限制
- **北交所 adj_factor quirk**：新上市股的 `adj_factor` 初始值给 1.0 而非真实倍率，导致 close × factor 跳变。启动扫描发现 2385 条
- **ingest 空 df 静默**：拉某些时段返回空 df 不报错，如果幂等逻辑误更新进度表会导致后续拉不回来（a-share-quant 踩过）
- **list_date 覆盖**：trade_cal 从 20160101 起，早于这个时间上市的股票要按日历日而不是交易日算"上市满 N 天"

## 与 AkShare 的关系

项目内评估（[[projects/2026-05-a-share-quant/notes/m2-decisions.md|M2 决策]]）：
- **Tushare**：接口稳定，字段规整，付费可靠
- **AkShare**：免费但底层爬取多个源（东财 / 新浪 / 同花顺），接口经常挂，字段不统一
- **决策**：**主 Tushare，AkShare 补龙虎榜 / 公告等 Tushare 未覆盖的领域**

## 与 llm-wiki 的关联

- [[projects/2026-05-a-share-quant/README|a-share-quant 项目]] 的**主数据源**
- [[quant-engine|quant-engine]] 通过 `quant_data/sources/tushare_source.py` adapter 封装
- 后续 A 股策略 project 都会继续使用

## 注册与配置

```bash
# 1. 注册 https://tushare.pro
# 2. 充值到 2000 积分档
# 3. .env 配置
TUSHARE_TOKEN=你的_token

# 4. Python 使用
import tushare as ts
ts.set_token(os.environ['TUSHARE_TOKEN'])
pro = ts.pro_api()
df = pro.daily(ts_code='600519.SH', start_date='20240101', end_date='20241231')
```

## 不覆盖的领域（要额外找）

- Tick / L2 订单簿：需更高积分或其他源
- 龙虎榜 / 公告文本：tushare 有但原文质量一般；实战常用 AkShare 的东财接口
- 海外股票深度数据：本 API 有但不如专业海外源
