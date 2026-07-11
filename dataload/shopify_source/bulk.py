"""Shopify GraphQL **Bulk Operations** の実行とJSONL整形ヘルパー。

Bulk API は1つのクエリでオブジェクトグラフ全体を非同期エクスポートし、結果を
JSONL (1行1ノード) で返す。ネストした connection の各ノードには ``__parentId`` が
付与され、親ノードを参照する。本モジュールは以下を提供する:

- ``run_bulk``: bulkOperationRunQuery を投入 → 完了までポーリング → JSONL を1行ずつ yield
- ``gid_type`` / ``clean_record``: gid から型を判定し、``__parentId`` を ``parent_id`` へ整形

Bulk の制約 (公式ドキュメント):
- 1クエリあたり connection は最大5、ネストは最大2階層
- connection のノードは Node インターフェース実装が必須 (id を持つ)
- ``first`` などのページング引数は無視される (全件エクスポート)
- 同一ショップで同時に実行できる bulk operation は1つのみ
"""

from __future__ import annotations

import json
import time
from typing import Any, Iterator

import requests

from .helpers import ShopifyGraphQLClient


class BulkOperationError(RuntimeError):
    pass


_RUN_MUTATION = """
mutation bulkRun($query: String!) {
  bulkOperationRunQuery(query: $query) {
    bulkOperation { id status }
    userErrors { field message }
  }
}
"""

_POLL_QUERY = """
query {
  currentBulkOperation {
    id status errorCode objectCount fileSize url partialDataUrl
  }
}
"""

_CANCEL_MUTATION = """
mutation bulkCancel($id: ID!) {
  bulkOperationCancel(id: $id) {
    bulkOperation { id status }
    userErrors { field message }
  }
}
"""

_TERMINAL_OK = {"COMPLETED"}
_TERMINAL_FAIL = {"FAILED", "CANCELED", "EXPIRED"}


def gid_type(gid: str) -> str:
    """``gid://shopify/ProductVariant/123`` → ``"ProductVariant"``。"""
    # 形式: gid://shopify/<Type>/<id>[?params]
    body = gid.split("?", 1)[0]
    parts = body.rstrip("/").split("/")
    return parts[-2] if len(parts) >= 2 else ""


def clean_record(record: dict[str, Any]) -> dict[str, Any]:
    """``__parentId`` を ``parent_id`` に改名し、dlt が扱いやすい素の dict にする。"""
    parent = record.pop("__parentId", None)
    if parent is not None:
        record["parent_id"] = parent
    return record


def _ensure_no_running_op(client: ShopifyGraphQLClient) -> None:
    """既存の RUNNING な bulk op があればキャンセルして解放する。"""
    op = client.execute(_POLL_QUERY, {}).get("currentBulkOperation")
    if op and op.get("status") in ("CREATED", "RUNNING"):
        client.execute(_CANCEL_MUTATION, {"id": op["id"]})
        # キャンセル反映待ち
        for _ in range(10):
            time.sleep(1)
            cur = client.execute(_POLL_QUERY, {}).get("currentBulkOperation")
            if not cur or cur.get("status") not in ("CREATED", "RUNNING", "CANCELING"):
                break


def run_bulk(
    client: ShopifyGraphQLClient,
    query: str,
    poll_interval: float = 3.0,
    timeout: float = 1800.0,
) -> Iterator[dict[str, Any]]:
    """Bulk query を実行し、結果 JSONL を1行ずつ (parse 済み dict) で yield する。"""
    _ensure_no_running_op(client)

    started = client.execute(_RUN_MUTATION, {"query": query})["bulkOperationRunQuery"]
    if started["userErrors"]:
        raise BulkOperationError(f"bulkOperationRunQuery: {started['userErrors']}")

    waited = 0.0
    op: dict[str, Any] = {}
    while True:
        time.sleep(poll_interval)
        waited += poll_interval
        op = client.execute(_POLL_QUERY, {})["currentBulkOperation"] or {}
        status = op.get("status")
        if status in _TERMINAL_OK:
            break
        if status in _TERMINAL_FAIL:
            raise BulkOperationError(f"bulk operation {status}: errorCode={op.get('errorCode')}")
        if waited >= timeout:
            raise BulkOperationError(f"bulk operation timeout after {timeout}s (status={status})")

    url = op.get("url")
    if not url:
        # 対象0件のとき url は null
        return
    yield from stream_jsonl(url)


def stream_jsonl(url: str, timeout: float = 120.0) -> Iterator[dict[str, Any]]:
    """署名付きURLの JSONL をストリーミングで1行ずつ parse して yield する。"""
    with requests.get(url, stream=True, timeout=timeout) as resp:
        resp.raise_for_status()
        for raw in resp.iter_lines():
            if raw:
                yield json.loads(raw)


def route_records(
    records: Iterator[dict[str, Any]],
    type_to_table: dict[str, str],
) -> Iterator[tuple[str, dict[str, Any]]]:
    """各レコードを gid の型からテーブル名へ振り分け、(table, clean_record) を yield する。

    ``type_to_table`` に無い型は無視する (想定外ノードの安全側スキップ)。
    """
    for rec in records:
        rid = rec.get("id")
        if not rid:
            continue
        table = type_to_table.get(gid_type(rid))
        if table is None:
            continue
        yield table, clean_record(rec)
