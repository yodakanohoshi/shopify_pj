"""Shopify Admin GraphQL クライアントとページング/整形ヘルパー。

認証は2方式に対応する:
- **Client Credentials Grant** (推奨): Dev Dashboard アプリの Client ID / Secret から
  アクセストークンを自動取得 (24時間で失効するため自動更新)。
- **静的トークン**: App Automation Token など固定トークンをそのまま利用。
"""

from __future__ import annotations

import time
from typing import Any, Iterator

import requests

# GraphQL のスロットル (leaky bucket) を考慮した既定リトライ回数
_MAX_RETRIES = 6
_DEFAULT_RESTORE_RATE = 50.0  # points/sec (Standard プラン既定)
_TOKEN_MARGIN = 120  # トークン失効の何秒前に更新するか


class ShopifyGraphQLError(RuntimeError):
    """userErrors 以外の GraphQL エラーをまとめて送出する。"""


class ShopifyGraphQLClient:
    """Admin GraphQL API への薄いクライアント。

    - Client Credentials Grant / 静的トークンの両対応 (X-Shopify-Access-Token)
    - THROTTLED / 5xx に対する指数バックオフ + コスト連動スリープ
    """

    def __init__(
        self,
        shop: str,
        api_version: str,
        access_token: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        timeout: int = 60,
    ):
        # shop は "my-store" でも "my-store.myshopify.com" でも受け付ける
        self.host = shop if shop.endswith(".myshopify.com") else f"{shop}.myshopify.com"
        self.endpoint = f"https://{self.host}/admin/api/{api_version}/graphql.json"

        self._static_token = access_token or None
        self._client_id = client_id or None
        self._client_secret = client_secret or None
        if not self._static_token and not (self._client_id and self._client_secret):
            raise ShopifyGraphQLError(
                "認証情報が未設定です。access_token、または client_id + client_secret を設定してください。"
            )

        self._session = requests.Session()
        self._session.headers.update({"Content-Type": "application/json"})
        self._timeout = timeout
        self._token: str | None = None
        self._token_expiry = 0.0

    # --- 認証 -------------------------------------------------------------
    def _access_token(self) -> str:
        if self._static_token:
            return self._static_token
        if self._token and time.monotonic() < self._token_expiry:
            return self._token
        resp = requests.post(
            f"https://{self.host}/admin/oauth/access_token",
            data={
                "grant_type": "client_credentials",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
            },
            timeout=30,
        )
        if resp.status_code >= 400:
            raise ShopifyGraphQLError(
                f"アクセストークン取得に失敗 (HTTP {resp.status_code})。"
                f"Client ID/Secret とアプリのストアへのインストールを確認してください。\n  応答: {resp.text[:400]}"
            )
        data = resp.json()
        self._token = data["access_token"]
        self._token_expiry = time.monotonic() + data.get("expires_in", 86399) - _TOKEN_MARGIN
        return self._token

    # --- 実行 -------------------------------------------------------------
    def execute(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        payload = {"query": query, "variables": variables}
        for attempt in range(_MAX_RETRIES):
            self._session.headers["X-Shopify-Access-Token"] = self._access_token()
            resp = self._session.post(self.endpoint, json=payload, timeout=self._timeout)

            # HTTP レベルのレート制限 / 一時エラー
            if resp.status_code in (429, 500, 502, 503, 504):
                self._sleep_backoff(attempt, resp)
                continue

            if resp.status_code >= 400:
                hint = ""
                if resp.status_code == 401:
                    hint = " — アクセストークンが無効か、アプリが対象ストアに未インストールです"
                elif resp.status_code == 403:
                    hint = " — アクセススコープ不足です"
                raise ShopifyGraphQLError(
                    f"HTTP {resp.status_code}{hint}\n  URL: {self.endpoint}\n  応答: {resp.text[:500]}"
                )
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
        throttle = body.get("extensions", {}).get("cost", {}).get("throttleStatus", {})
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
