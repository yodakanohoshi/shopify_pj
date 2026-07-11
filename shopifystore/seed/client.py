"""Shopify Admin GraphQL クライアント (シード投入用・書き込み対応)。"""

from __future__ import annotations

import os
import time
from typing import Any

import requests
from dotenv import load_dotenv


class AdminAPIError(RuntimeError):
    pass


class UserError(RuntimeError):
    """mutation の userErrors を表す。"""


class ShopifyAdmin:
    def __init__(self, shop: str | None = None, token: str | None = None, api_version: str | None = None):
        load_dotenv()
        shop = shop or os.environ["SHOPIFY_SHOP"]
        token = token or os.environ["SHOPIFY_ADMIN_TOKEN"]
        api_version = api_version or os.getenv("SHOPIFY_API_VERSION", "2025-01")
        host = shop if shop.endswith(".myshopify.com") else f"{shop}.myshopify.com"
        self.endpoint = f"https://{host}/admin/api/{api_version}/graphql.json"
        self._session = requests.Session()
        self._session.headers.update(
            {"Content-Type": "application/json", "X-Shopify-Access-Token": token}
        )

    def execute(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        for attempt in range(6):
            resp = self._session.post(
                self.endpoint, json={"query": query, "variables": variables or {}}, timeout=60
            )
            if resp.status_code in (429, 500, 502, 503, 504):
                time.sleep(min(2**attempt, 20))
                continue
            resp.raise_for_status()
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
