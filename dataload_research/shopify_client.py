"""調査用の最小 Shopify Admin GraphQL クライアント (自己完結)。

本番の ``dataload/shopify_source/helpers.py`` を薄く写した調査サンドボックス版。
認証は Client Credentials Grant か静的トークンのいずれか。スロットル制御は
簡易 (429/THROTTLED を指数バックオフ) に留め、少量取得の実験に振り切っている。
"""

from __future__ import annotations

import os
import time
from typing import Any

import requests
from dotenv import load_dotenv

_MAX_RETRIES = 5


class ResearchClientError(RuntimeError):
    pass


class ShopifyClient:
    def __init__(
        self,
        shop: str,
        api_version: str,
        access_token: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        timeout: int = 60,
    ):
        self.host = shop if shop.endswith(".myshopify.com") else f"{shop}.myshopify.com"
        self.endpoint = f"https://{self.host}/admin/api/{api_version}/graphql.json"
        self._static_token = access_token or None
        self._client_id = client_id or None
        self._client_secret = client_secret or None
        if not self._static_token and not (self._client_id and self._client_secret):
            raise ResearchClientError(
                "認証情報が未設定です。SHOPIFY_ACCESS_TOKEN か "
                "SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET を .env に設定してください。"
            )
        self._session = requests.Session()
        self._session.headers.update({"Content-Type": "application/json"})
        self._timeout = timeout
        self._token: str | None = None

    # --- 認証 ---
    def _access_token(self) -> str:
        if self._static_token:
            return self._static_token
        if self._token:
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
            raise ResearchClientError(
                f"アクセストークン取得に失敗 (HTTP {resp.status_code}): {resp.text[:300]}"
            )
        self._token = resp.json()["access_token"]
        return self._token

    # --- 実行 ---
    def execute(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = {"query": query, "variables": variables or {}}
        for attempt in range(_MAX_RETRIES):
            self._session.headers["X-Shopify-Access-Token"] = self._access_token()
            resp = self._session.post(self.endpoint, json=payload, timeout=self._timeout)
            if resp.status_code in (429, 500, 502, 503, 504):
                time.sleep(min(2**attempt, 20))
                continue
            if resp.status_code >= 400:
                raise ResearchClientError(f"HTTP {resp.status_code}: {resp.text[:400]}")
            body = resp.json()
            errors = body.get("errors")
            if errors:
                if any(e.get("extensions", {}).get("code") == "THROTTLED" for e in errors):
                    time.sleep(min(2**attempt, 10))
                    continue
                raise ResearchClientError(str(errors))
            return body["data"]
        raise ResearchClientError(f"リトライ上限 ({_MAX_RETRIES}) 到達")


def client_from_env() -> ShopifyClient:
    """``.env`` / 環境変数から調査用クライアントを組み立てる。"""
    load_dotenv()
    return ShopifyClient(
        shop=os.environ["SHOPIFY_SHOP"],
        api_version=os.getenv("SHOPIFY_API_VERSION", "2026-07"),
        access_token=os.getenv("SHOPIFY_ACCESS_TOKEN"),
        client_id=os.getenv("SHOPIFY_CLIENT_ID"),
        client_secret=os.getenv("SHOPIFY_CLIENT_SECRET"),
    )
