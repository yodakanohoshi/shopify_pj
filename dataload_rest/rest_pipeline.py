"""REST API → DuckDB (raw) ロードのエントリポイント。

`dataload/shopify_pipeline.py` と同じ運用を、通常の REST + ページングで行う。

    # 差分取得 (既定・日次/毎時のスケジュール実行向け)
    uv run python rest_pipeline.py

    # 全期間バックフィル (手動・随時)
    uv run python rest_pipeline.py --backfill

    # 期間指定バックフィル (手動・随時)
    uv run python rest_pipeline.py --start 2025-01-01 --end 2025-03-31

差分取得は前回実行で記録した高水位以降だけを API 側のクエリパラメータで絞って取得し
merge する (初回は高水位が無いため全件 = 初回バックフィル)。

認証情報は ``.dlt/secrets.toml`` もしくは環境変数で与える。
``.env`` があれば読み込み、``REST_*`` を dlt が解釈する形へブリッジする。
"""

from __future__ import annotations

import argparse
import os

import dlt
from dotenv import load_dotenv

from rest_source import rest_api_source

# DuckDB ファイル。Shopify 版と同居させる場合は同じ物理ファイルを指してもよい。
DUCKDB_PATH = os.getenv("REST_DUCKDB_PATH", "rest_api.duckdb")
RAW_DATASET = "raw"


def _bridge_env() -> None:
    """`.env` の REST_* を dlt の設定キーへ橋渡しする (任意)。"""
    load_dotenv()
    mapping = {
        "REST_BASE_URL": "SOURCES__REST_API__BASE_URL",
        "REST_ACCESS_TOKEN": "SOURCES__REST_API__ACCESS_TOKEN",
        "REST_CLIENT_ID": "SOURCES__REST_API__CLIENT_ID",
        "REST_CLIENT_SECRET": "SOURCES__REST_API__CLIENT_SECRET",
        "REST_TOKEN_URL": "SOURCES__REST_API__TOKEN_URL",
        "REST_SCOPE": "SOURCES__REST_API__SCOPE",
    }
    for src, dst in mapping.items():
        if os.getenv(src) and not os.getenv(dst):
            os.environ[dst] = os.environ[src]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="REST API → DuckDB (raw) ロード")
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
        pipeline_name="rest_api",
        destination=dlt.destinations.duckdb(DUCKDB_PATH),
        dataset_name=RAW_DATASET,
        progress="log",
    )

    load_info = pipeline.run(
        rest_api_source(start_date=start_date, end_date=end_date, backfill=backfill)
    )
    print(load_info)


if __name__ == "__main__":
    args = _parse_args()
    run(backfill=args.backfill, start_date=args.start, end_date=args.end)
