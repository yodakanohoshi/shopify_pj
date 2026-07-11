"""Shopify → DuckDB (raw) ロードのエントリポイント。

使い方::

    uv run python shopify_pipeline.py

認証情報は ``.dlt/secrets.toml`` もしくは環境変数で与える。
``.env`` があれば読み込み、``SHOPIFY_*`` を dlt が解釈する形へブリッジする。
"""

from __future__ import annotations

import os

import dlt
from dotenv import load_dotenv

from shopify_source import shopify_source

# DuckDB ファイル。elt/ の dbt profiles.yml と同じ物理ファイルを指す。
DUCKDB_PATH = os.getenv("SHOPIFY_DUCKDB_PATH", "shopify.duckdb")
RAW_DATASET = "raw"


def _bridge_env() -> None:
    """`.env` の SHOPIFY_* を dlt の設定キーへ橋渡しする (任意)。"""
    load_dotenv()
    mapping = {
        "SHOPIFY_SHOP": "SOURCES__SHOPIFY__SHOP",
        "SHOPIFY_ACCESS_TOKEN": "SOURCES__SHOPIFY__ACCESS_TOKEN",
        "SHOPIFY_API_VERSION": "SOURCES__SHOPIFY__API_VERSION",
        "SHOPIFY_START_DATE": "SOURCES__SHOPIFY__START_DATE",
    }
    for src, dst in mapping.items():
        if os.getenv(src) and not os.getenv(dst):
            os.environ[dst] = os.environ[src]


def run() -> None:
    _bridge_env()

    pipeline = dlt.pipeline(
        pipeline_name="shopify",
        destination=dlt.destinations.duckdb(DUCKDB_PATH),
        dataset_name=RAW_DATASET,
        progress="log",
    )

    load_info = pipeline.run(shopify_source())
    print(load_info)


if __name__ == "__main__":
    run()
