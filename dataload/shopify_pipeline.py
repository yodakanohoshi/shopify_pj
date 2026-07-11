"""Shopify → DuckDB (raw) ロードのエントリポイント。

想定運用は2モード:

    # 差分取得 (既定・日次/毎時のスケジュール実行向け)
    uv run python shopify_pipeline.py

    # 全期間バックフィル (手動・随時)
    uv run python shopify_pipeline.py --backfill

    # 期間指定バックフィル (手動・随時)
    uv run python shopify_pipeline.py --start 2025-01-01 --end 2025-03-31

差分取得は前回実行で記録した高水位以降だけを Bulk 側フィルタで絞って取得し merge する
(初回は高水位が無いため全件 = 初回バックフィル)。

認証情報は ``.dlt/secrets.toml`` もしくは環境変数で与える。
``.env`` があれば読み込み、``SHOPIFY_*`` を dlt が解釈する形へブリッジする。
"""

from __future__ import annotations

import argparse
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
        "SHOPIFY_CLIENT_ID": "SOURCES__SHOPIFY__CLIENT_ID",
        "SHOPIFY_CLIENT_SECRET": "SOURCES__SHOPIFY__CLIENT_SECRET",
        "SHOPIFY_API_VERSION": "SOURCES__SHOPIFY__API_VERSION",
    }
    for src, dst in mapping.items():
        if os.getenv(src) and not os.getenv(dst):
            os.environ[dst] = os.environ[src]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Shopify → DuckDB (raw) ロード")
    parser.add_argument(
        "--backfill",
        action="store_true",
        help="保存済み高水位を無視して全期間を再取得する (手動バックフィル)",
    )
    parser.add_argument(
        "--start",
        metavar="ISO_DATE",
        help="バックフィルの下限 (例 2025-01-01)。指定するとバックフィル扱い",
    )
    parser.add_argument(
        "--end",
        metavar="ISO_DATE",
        help="バックフィルの上限 (例 2025-03-31)",
    )
    return parser.parse_args()


def run(backfill: bool = False, start_date: str | None = None, end_date: str | None = None) -> None:
    _bridge_env()

    pipeline = dlt.pipeline(
        pipeline_name="shopify",
        destination=dlt.destinations.duckdb(DUCKDB_PATH),
        dataset_name=RAW_DATASET,
        progress="log",
    )

    load_info = pipeline.run(
        shopify_source(start_date=start_date, end_date=end_date, backfill=backfill)
    )
    print(load_info)


if __name__ == "__main__":
    args = _parse_args()
    run(backfill=args.backfill, start_date=args.start, end_date=args.end)
