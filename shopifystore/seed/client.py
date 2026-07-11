"""Shopify Admin GraphQL クライアント (シード投入用・書き込み対応)。

認証は2方式に対応する:
- **Client Credentials Grant** (推奨): Dev Dashboard アプリの Client ID / Secret から
  アクセストークンを自動取得 (24時間で失効するため自動更新)。
- **静的トークン**: App Automation Token など、そのまま使える固定トークン。

いずれか一方を .env に設定する:
- `SHOPIFY_CLIENT_ID` + `SHOPIFY_CLIENT_SECRET`  (client credentials)
- もしくは `SHOPIFY_ADMIN_TOKEN`                  (静的トークン)
"""

from __future__ import annotations

import os
import time
from typing import Any

import requests
from dotenv import load_dotenv

_TOKEN_MARGIN = 120  # 失効の何秒前に更新するか


class AdminAPIError(RuntimeError):
    pass


class UserError(RuntimeError):
    """mutation の userErrors を表す。"""


class ShopifyAdmin:
    def __init__(self, shop: str | None = None, api_version: str | None = None):
        load_dotenv()
        shop = shop or os.environ["SHOPIFY_SHOP"]
        self.host = shop if shop.endswith(".myshopify.com") else f"{shop}.myshopify.com"
        self.api_version = api_version or os.getenv("SHOPIFY_API_VERSION", "2025-01")
        self.endpoint = f"https://{self.host}/admin/api/{self.api_version}/graphql.json"

        self._static_token = os.getenv("SHOPIFY_ADMIN_TOKEN") or None
        self._client_id = os.getenv("SHOPIFY_CLIENT_ID") or None
        self._client_secret = os.getenv("SHOPIFY_CLIENT_SECRET") or None
        if not self._static_token and not (self._client_id and self._client_secret):
            raise AdminAPIError(
                "認証情報が未設定です。.env に SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET "
                "(Dev Dashboard アプリ)、または SHOPIFY_ADMIN_TOKEN を設定してください。"
            )

        self._session = requests.Session()
        self._session.headers.update({"Content-Type": "application/json"})
        self._token: str | None = None
        self._token_expiry = 0.0

    # --- 認証 -------------------------------------------------------------
    def _access_token(self) -> str:
        if self._static_token:
            return self._static_token
        if self._token and time.monotonic() < self._token_expiry:
            return self._token
        # Client Credentials Grant でアクセストークンを取得
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
            raise AdminAPIError(
                f"アクセストークン取得に失敗 (HTTP {resp.status_code})。"
                f"Client ID/Secret とアプリのストアへのインストールを確認してください。\n  応答: {resp.text[:400]}"
            )
        data = resp.json()
        self._token = data["access_token"]
        self._token_expiry = time.monotonic() + data.get("expires_in", 86399) - _TOKEN_MARGIN
        return self._token

    # --- 実行 -------------------------------------------------------------
    def execute(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        for attempt in range(6):
            self._session.headers["X-Shopify-Access-Token"] = self._access_token()
            resp = self._session.post(
                self.endpoint, json={"query": query, "variables": variables or {}}, timeout=60
            )
            if resp.status_code in (429, 500, 502, 503, 504):
                time.sleep(min(2**attempt, 20))
                continue
            if resp.status_code >= 400:
                hint = ""
                if resp.status_code == 401:
                    hint = " — トークンが無効か、アプリが対象ストアに未インストールです"
                elif resp.status_code == 403:
                    hint = " — アクセススコープ不足です"
                raise AdminAPIError(
                    f"HTTP {resp.status_code}{hint}\n  URL: {self.endpoint}\n  応答: {resp.text[:500]}"
                )
            body = resp.json()
            if body.get("errors"):
                if any(e.get("extensions", {}).get("code") == "THROTTLED" for e in body["errors"]):
                    time.sleep(min(2**attempt, 10))
                    continue
                raise AdminAPIError(str(body["errors"]))
            return body["data"]
        raise AdminAPIError("リトライ上限に到達")

    def mutate(self, query: str, variables: dict[str, Any], result_key: str) -> dict[str, Any]:
        """mutation を実行し userErrors を検査して結果ペイロードを返す。"""
        data = self.execute(query, variables)
        payload = data[result_key]
        errors = payload.get("userErrors") or []
        if errors:
            raise UserError(f"{result_key}: {errors}")
        return payload
