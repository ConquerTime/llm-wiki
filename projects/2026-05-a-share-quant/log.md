# A 股量化策略 · 活动日志

> 追加式时间线，记录讨论、决策、产出、阻塞。

---

## [2026-05-08] 启动
- 项目创建，目录初始化（raw/ notes/ deliverables/）
- 与用户对齐：
  - 核心目标 = 实盘策略开发（非纯研究、非纯学习）
  - 交付物 = 数据管道 + 可跑回测代码 + 综述文档 + 策略笔记
  - 短名 = a-share-quant（英文，宽泛，便于长期使用）
  - 外部关联 = 无，纯新起
- 非目标已写入 brief：不做高频、不做非 A 股、不做黑箱 ML 主线、不做完整执行系统
- 下一步：M1 方向选型，先做策略思路调研

## [2026-05-08] M1 方向选型 · 进行中
- 对齐个人画像：100–500 万 / 盘中高频关注 / 进攻型年化 30%+ 容忍 30% 回撤 / 无方向倾向
- 产出约束锚点：[[projects/2026-05-a-share-quant/notes/m1-constraints.md|m1-constraints]]
- 产出策略家族调研：[[projects/2026-05-a-share-quant/notes/m1-strategy-families.md|m1-strategy-families]]
- **推荐主方向**：时序趋势 / 动量 + 事件驱动过滤器
- **备选方向**：小市值多因子（进攻版，仅主方向失败时启用）
- 明确排除：均值回归、统计套利（做空受限）、纯打板（监管 + 盯盘质量）
- 待用户确认：主方向选型是否采纳；采纳后升级到 deliverables/strategy-selection.md

## [2026-05-08] M2 数据管道 · 骨架落地
- 决策对齐：Tushare Pro 主 + AkShare 补 / DuckDB / 10 年全市场 / Python 3.11 + uv
- 决策记录：[[projects/2026-05-a-share-quant/notes/m2-decisions.md|m2-decisions]]
- 代码骨架：`deliverables/data-pipeline/`
  - `quant_data/sources/` tushare + akshare adapter（拉数）
  - `quant_data/storage/duckdb_store.py` DuckDB schema + 幂等 upsert + 进度表
  - `quant_data/ingest/` 日线 + 复权 + 每日基础 + 财务的增量编排
  - `quant_data/api.py` 统一读数 API（含前复权动态计算、ann_date 防前瞻）
  - `scripts/bootstrap.py` + `scripts/daily_update.py`
  - `README.md` 使用说明
- 所有 Python 文件语法检查通过
- 待用户：注册 Tushare Pro 账号、配置 TUSHARE_TOKEN，跑 `--smoke` 验证通路
