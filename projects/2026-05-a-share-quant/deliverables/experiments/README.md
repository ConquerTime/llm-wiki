# Experiments · A-share Quant

本 project 的所有回测 Spike 和实验脚本 / 产物。

## 边界

- **本目录 = a-share-quant project 专属**，与 `../data-pipeline/`（引擎）边界清晰
- 引擎：可复用基础设施（数据管道、回测引擎、因子、样本池）
- 实验：本 project 的策略探索（hello-world、M4 Spike A-H ...）

下一个 A 股策略 project 启动时：
- 新 project 自己开 `experiments/` 放它的实验
- 引擎仍从 `../../2026-05-a-share-quant/deliverables/data-pipeline/` 共享

## 运行

```bash
# 从本目录启动（需要引擎已经 uv sync 过）
cd deliverables/experiments
../data-pipeline/.venv/bin/python -m scripts.m4_spike --which F
../data-pipeline/.venv/bin/python -m scripts.hello_world --ts-code 600519.SH
```

脚本内部 `sys.path.insert(0, ENGINE_ROOT)` 会自动把 `data-pipeline/` 放进 import 路径。

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
