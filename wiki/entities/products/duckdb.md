---
title: DuckDB
type: entity
subtype: product
tags: [tool, programming]
created: 2026-05-09
updated: 2026-05-09
sources:
  - "[[projects/2026-05-a-share-quant/retro.md|2026-05 a-share-quant 项目复盘]]"
  - "[[projects/2026-05-a-share-quant/notes/m2-decisions.md|M2 数据管道决策]]"
---

# DuckDB

> 嵌入式列存 SQL 数据库。面向分析场景的 SQLite —— 单文件、零配置、pandas 原生互通、百万行秒级聚合。

## 基本事实

- **官网**：https://duckdb.org
- **定位**：Embedded OLAP database（分析型嵌入式数据库）
- **类比**：**SQLite for analytics** —— 单文件、零服务、无需 schema 预先设计
- **语言**：C++ 核心，Python / R / JS / Rust 等一等绑定
- **License**：MIT
- **发布**：2019 起，Mark Raasveldt & Hannes Mühleisen（CWI Amsterdam）
- **核心差异 vs SQLite**：列存 + 向量化执行 + pandas 原生互通

## 为什么在数据分析场景完胜 SQLite

| 维度 | SQLite | DuckDB |
|---|---|---|
| 存储 | 行存 | **列存** |
| 执行 | 逐行解释 | **向量化（SIMD）** |
| 聚合大表 | 慢（全行扫描）| **快（列扫描 + 并行）** |
| pandas 互通 | 需显式转换 | **零拷贝（Arrow）** |
| 并发写 | 单写多读 | 单写多读（相似）|
| 事务 | ACID | ACID |

**典型场景差**：1000 万行做 GROUP BY，SQLite 几分钟，DuckDB 几秒。

## 项目内的使用（a-share-quant）

- 文件：`practices/quant-investing/engine/data/quant.duckdb`，**2.2 GB 存 7 张表**
- 全市场 **5838 只 × 10 年 ≈ 1060 万行**
- 典型查询性能：
  - 全市场一次读入：~3.5s
  - 按日期聚合：~1s
  - Rolling window join：~5s
- 关键操作：[[quant-engine|quant-engine]] 的 `quant_data/storage/duckdb_store.py` ~200 行封装了 schema + 幂等 upsert + 进度表

## 踩过的坑（来自 [[projects/2026-05-a-share-quant/notes/m2-decisions.md|M2 实战]]）

- **`CURRENT_TIMESTAMP` 误解析**：在某些上下文被当成列名而非函数。改用 `now()`
- **`CAST('19910403' AS DATE)` 不支持 YYYYMMDD**：要用 `strptime(date_str, '%Y%m%d')`
- **`ON CONFLICT` 支持有限**（1.1 版）：主键冲突用 `delete-then-insert` 替代
- **`INTERVAL '1 YEAR'` 与 `date_add` 混用**：SQL 方言差异大，建议统一用标准 INTERVAL 语法

## 为什么 a-share-quant 选 DuckDB 而不是其他

[[projects/2026-05-a-share-quant/notes/m2-decisions.md|M2 决策]] 对比：

| 选项 | 淘汰原因 |
|---|---|
| **PostgreSQL / MySQL** | 需起服务；列存需 CStore 扩展；对单机分析过重 |
| **SQLite** | 行存，千万行聚合慢；对本场景不够快 |
| **Parquet + pandas** | 没有 SQL / 事务；多次查询要重读全文件 |
| **qlib binary** | 自家格式；只给 qlib 用 |
| **ClickHouse** | 分布式太重；本场景单机就够 |
| **DuckDB** | 单文件、列存、SQL 齐、pandas 零拷贝、零运维 |

**关键判断**：个人项目 + 单机 + 2-10 GB 数据量 + 频繁聚合 —— DuckDB 是当前最合适的点。

## 适用场景

✓ 数据分析 / 回测 / 科研单机工作流
✓ pandas pipeline 里想"突然写段 SQL 做聚合"
✓ 单文件可版本控制（Git LFS）或同步

✗ 高并发 OLTP（用 Postgres）
✗ 跨机分布式（用 ClickHouse / Doris）
✗ 流式数据（用 kdb+ / Druid）

## 与 llm-wiki 的关联

- [[projects/2026-05-a-share-quant/README|a-share-quant 项目]] 的存储层
- [[quant-engine|quant-engine]] 核心依赖之一
- 未来任何"单机 + 大表 + SQL"场景的首选
