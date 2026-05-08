"""Configuration for the data pipeline."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# 仓库根（data-pipeline 的父目录）
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PIPELINE_ROOT / "data"
DB_PATH = DATA_DIR / "quant.duckdb"

# 显式指向 data-pipeline 下的 .env，不依赖 cwd
load_dotenv(dotenv_path=PIPELINE_ROOT / ".env")

# 数据范围
START_DATE = "20160101"  # YYYYMMDD
# END_DATE 留空 = 拉到最新交易日

# Tushare token
TUSHARE_TOKEN = os.environ.get("TUSHARE_TOKEN", "")


@dataclass(frozen=True)
class Config:
    db_path: Path = DB_PATH
    start_date: str = START_DATE
    tushare_token: str = TUSHARE_TOKEN

    def require_token(self) -> str:
        if not self.tushare_token:
            raise RuntimeError(
                "TUSHARE_TOKEN 未设置。请在 .env 或环境变量中配置，"
                "获取方式见 https://tushare.pro"
            )
        return self.tushare_token


CONFIG = Config()


def ensure_data_dir() -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR
