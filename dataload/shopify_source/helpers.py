"""Shopify Admin GraphQL クライアントとページング/整形ヘルパー。"""

from __future__ import annotations

import time
from typing import Any, Iterator

import requests

# GraphQL のスロットル (leaky bucket) を考慮した既定リトライ回数
_MAX_RETRIES = 6
_DEFAULT_RESTORE_RATE = 50.0  # points/sec (Standard プラン既定)


class ShopifyGraphQLError(RuntimeError):
    """userErrors 以外の GraphQL エラーをまとめて送出する。"""


class ShopifyGraphQLClient:
    """Admin GraphQL API への薄いクライアント。

    - X-Shopify-Access-Token 認証
    - THROTTLED / 5xx に対する指数バックオフ + コスト連動スリープ
    """

    def __init__(self, shop: str, access_token: str, api_version: str, timeout: int = 60):
        # shop は "my-store" でも "my-store.myshopify.com" でも受け付ける
        host = shop if shop.endswith(".myshopify.com") else f"{shop}.myshopify.com"
        self.endpoint = f"https://{host}/admin/api/{api_version}/graphql.json"
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Content-Type": "application/json",
                "X-Shopify-Access-Token": access_token,
            }
        )
        self._timeout = timeout

    def execute(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        payload = {"query": query, "variables": variables}
        for attempt in range(_MAX_RETRIES):
            resp = self._session.post(self.endpoint, json=payload, timeout=self._timeout)

            # HTTP レベルのレート制限 / 一時エラー
            if resp.status_code in (429, 500, 502, 503, 504):
                self._sleep_backoff(attempt, resp)
                continue

            resp.raise_for_status()
            body = resp.json()

            errors = body.get("errors")
            if errors:
                # GraphQL の THROTTLED はレート制限。待って再試行する。
                if any(e.get("extensions", {}).get("code") == "THROTTLED" for e in errors):
                    self._sleep_on_cost(body, attempt)
                    continue
                raise ShopifyGraphQLError(str(errors))

            self._respect_cost(body)
            return body["data"]

        raise ShopifyGraphQLError(f"GraphQL リトライ上限 ({_MAX_RETRIES}) 到達: {self.endpoint}")

    # --- スロットル制御 ---------------------------------------------------
    @staticmethod
    def _sleep_backoff(attempt: int, resp: requests.Response) -> None:
        retry_after = resp.headers.get("Retry-After")
        wait = float(retry_after) if retry_after else min(2**attempt, 30)
        time.sleep(wait)

    @staticmethod
    def _sleep_on_cost(body: dict[str, Any], attempt: int) -> None:
        throttle = (
            body.get("extensions", {}).get("cost", {}).get("throttleStatus", {})
        )
        requested = throttle.get("requestedQueryCost", 100)
        available = throttle.get("currentlyAvailable", 0)
        restore = throttle.get("restoreRate", _DEFAULT_RESTORE_RATE) or _DEFAULT_RESTORE_RATE
        deficit = max(requested - available, 0)
        time.sleep(max(deficit / restore, min(2**attempt, 10)))

    @staticmethod
    def _respect_cost(body: dict[str, Any]) -> None:
        """次リクエストで確実に枯渇しないよう、残量が少なければ軽く待つ。"""
        throttle = body.get("extensions", {}).get("cost", {}).get("throttleStatus", {})
        available = throttle.get("currentlyAvailable")
        requested = throttle.get("requestedQueryCost", 0)
        restore = throttle.get("restoreRate", _DEFAULT_RESTORE_RATE) or _DEFAULT_RESTORE_RATE
        if available is not None and available < requested:
            time.sleep((requested - available) / restore)


def paginate(
    client: ShopifyGraphQLClient,
    query: str,
    root_field: str,
    query_filter: str | None = None,
    page_size: int = 100,
) -> Iterator[dict[str, Any]]:
    """トップレベル connection をカーソルページングし、整形済みノードを yield する。"""
    after: str | None = None
    while True:
        variables = {"first": page_size, "after": after, "query": query_filter}
        data = client.execute(query, variables)
        connection = data[root_field]
        for edge in connection["edges"]:
            yield unwrap_connections(edge["node"])
        page_info = connection["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        after = page_info["endCursor"]


def unwrap_connections(value: Any) -> Any:
    """GraphQL の ``{edges:[{node:{...}}], pageInfo}`` 構造を素直なリストへ再帰変換する。

    dlt が自然な子テーブルを生成できるよう、``edges/node/cursor`` の入れ子を畳む。
    """
    if isinstance(value, dict):
        if "edges" in value and isinstance(value["edges"], list):
            return [unwrap_connections(e.get("node", e)) for e in value["edges"]]
        return {k: unwrap_connections(v) for k, v in value.items() if k != "pageInfo"}
    if isinstance(value, list):
        return [unwrap_connections(v) for v in value]
    return value
