# Experiments · A-share Quant

本 project 的所有回测 Spike 和实验脚本 / 产物。

## 边界

- **本目录 = a-share-quant project 专属**，不跨 project 共享
- **引擎**（数据管道 / 回测 / 因子 / 样本池）已于 2026-05-09 迁到 `practices/quant-investing/engine/`，跨 project 共享
- 实验：本 project 的策略探索（hello-world、M4 Spike A-H3）

下一个 A 股策略 project 启动时：
- 新 project 自己开 `experiments/` 放它的实验
- 引擎从 `practices/quant-investing/engine/` 共享
- 参见 [[quant-engine|quant-engine 实体页]]

## 运行

```bash
# 从本目录启动
cd deliverables/experiments
/Users/.../practices/quant-investing/engine/.venv/bin/python -m scripts.m4_spike --which F
/Users/.../practices/quant-investing/engine/.venv/bin/python -m scripts.hello_world --ts-code 600519.SH
```

脚本内部自动解析 `VAULT_ROOT / practices / quant-investing / engine` 为 `ENGINE_ROOT` 并加 sys.path。

## 实验清单

| 脚本 | 对应文档 | 用途 |
|---|---|---|
| `scripts/hello_world.py` | [[../../notes/m3-hello-world.md]] / [[../../notes/m3-hello-world-v2.md]] | M3 hello-world（茅台 SMA / 510300 ETF）|
| `scripts/m4_spike.py` | [[../../notes/m4-spike-spec.md]] 及后续各 results | M4 Spike A-H 全链 |

## 产物（`data/`）

每个 Spike 产出两个文件：
- `m4_spike_{X}.json`：配置参数 + 核心指标
- `m4_spike_{X}.csv`：每日 NAV + 基准 NAV 时间序列（供作图）

Spike 图存在上级的 `../../notes/` 里（属于报告资产）。

## 目录结构

```
experiments/
├── README.md              # 本文件
├── scripts/
│   ├── __init__.py
│   ├── hello_world.py     # M3
│   └── m4_spike.py        # M4 Spike A-H
└── data/
    ├── hello_world*.{csv,json}
    └── m4_spike_*.{csv,json}
```
