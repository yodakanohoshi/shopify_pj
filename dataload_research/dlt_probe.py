"""dlt で数件だけロードし、dlt が生成する正規化スキーマを確認する。

``raw_probe.py`` が API の生 JSON を見るのに対し、こちらは **dlt がその JSON を
どうテーブル化するか** (tags → 子テーブル、ネスト → ``親__子`` 平坦化 等) を確認する。
本番 (``dataload/``) は Bulk 主体だが、ここでは非 Bulk の少量取得で挙動を素早く覗く。

``research.duckdb`` (dataset: ``research``) にロードし、生成テーブルと列を一覧表示する。
本番の ``shopify.duckdb`` とは別ファイルなので汚さない。

使い方::

    uv run python dlt_probe.py                 # 全プローブを 3 件ずつ
    uv run python dlt_probe.py --only products -n 5
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Iterator

import dlt

from queries import PROBES
from raw_probe import _unwrap
from shopify_client import client_from_env

DUCKDB_PATH = str(Path(__file__).parent / "research.duckdb")


@dlt.source(name="shopify_research")
def research_source(targets: list[str], n: int):
    client = client_from_env()

    def make(name: str):
        root_field, query = PROBES[name]

        @dlt.resource(name=name, write_disposition="replace")
        def resource() -> Iterator[dict[str, Any]]:
            data = client.execute(query, {"n": n})
            yield from _unwrap(data[root_field])

        return resource

    return [make(name) for name in targets]


def _print_schema(pipeline: dlt.Pipeline) -> None:
    dataset = pipeline.dataset_name
    with pipeline.sql_client() as sql:
        rows = sql.execute_sql(
            """
            select table_name, column_name, data_type
            from information_schema.columns
            where table_schema = %s
            order by table_name, ordinal_position
            """,
            dataset,
        )
    print(f"\n=== 生成テーブル (schema: {dataset}) ===")
    current = None
    for table, column, dtype in rows:
        if table != current:
            print(f"\n[{table}]")
            current = table
        print(f"  {column}: {dtype}")


def main() -> None:
    parser = argparse.ArgumentParser(description="dlt で数件ロードし正規化スキーマを確認する")
    parser.add_argument("--only", nargs="*", metavar="NAME", help="対象プローブ (既定: 全部)")
    parser.add_argument("-n", type=int, default=3, help="取得件数 (既定 3)")
    args = parser.parse_args()

    targets = args.only or list(PROBES)
    unknown = [t for t in targets if t not in PROBES]
    if unknown:
        raise SystemExit(f"未知のプローブ: {unknown}")

    pipeline = dlt.pipeline(
        pipeline_name="shopify_research",
        destination=dlt.destinations.duckdb(DUCKDB_PATH),
        dataset_name="research",
    )
    load_info = pipeline.run(research_source(targets, args.n))
    print(load_info)
    _print_schema(pipeline)


if __name__ == "__main__":
    main()
