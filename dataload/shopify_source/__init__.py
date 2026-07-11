"""Shopify Admin GraphQL を対象とした dlt ソース。

標準リソース (orders / customers / products) に加え、dlt 標準ソースが未対応の
**discounts** (discountNodes) をカスタムリソースとして提供する。

すべて ``updatedAt`` ベースの増分ロードに対応。初回は ``start_date`` 以降を全件、
2回目以降は前回カーソル (last_value) 以降のみ取得する。
"""

from __future__ import annotations

from typing import Any, Iterable, Iterator

import dlt
from dlt.sources import DltResource

from .helpers import ShopifyGraphQLClient, paginate
from . import queries

DEFAULT_START_DATE = "2020-01-01T00:00:00Z"


def _build_query_filter(incremental: dlt.sources.incremental, field: str = "updated_at") -> str | None:
    """dlt incremental の last_value を Shopify 検索構文へ変換する。"""
    last_value = incremental.last_value
    if not last_value:
        return None
    # Shopify の検索は ISO8601 を受け付ける。境界は >= にして取りこぼしを防ぐ。
    return f"{field}:>='{last_value}'"


@dlt.source(name="shopify")
def shopify_source(
    shop: str = dlt.config.value,
    access_token: str = dlt.secrets.value,
    api_version: str = "2025-01",
    start_date: str = DEFAULT_START_DATE,
    page_size: int = 100,
) -> Iterable[DltResource]:
    """Shopify の主要オブジェクトを raw スキーマへロードするソース。"""

    client = ShopifyGraphQLClient(shop=shop, access_token=access_token, api_version=api_version)

    def _paged(query: str, root_field: str, incremental: dlt.sources.incremental) -> Iterator[dict[str, Any]]:
        query_filter = _build_query_filter(incremental)
        yield from paginate(client, query, root_field, query_filter=query_filter, page_size=page_size)

    @dlt.resource(name="orders", primary_key="id", write_disposition="merge")
    def orders(
        updated_at: dlt.sources.incremental[str] = dlt.sources.incremental(
            "updatedAt", initial_value=start_date
        ),
    ) -> Iterator[dict[str, Any]]:
        yield from _paged(queries.ORDERS, "orders", updated_at)

    @dlt.resource(name="customers", primary_key="id", write_disposition="merge")
    def customers(
        updated_at: dlt.sources.incremental[str] = dlt.sources.incremental(
            "updatedAt", initial_value=start_date
        ),
    ) -> Iterator[dict[str, Any]]:
        yield from _paged(queries.CUSTOMERS, "customers", updated_at)

    @dlt.resource(name="products", primary_key="id", write_disposition="merge")
    def products(
        updated_at: dlt.sources.incremental[str] = dlt.sources.incremental(
            "updatedAt", initial_value=start_date
        ),
    ) -> Iterator[dict[str, Any]]:
        yield from _paged(queries.PRODUCTS, "products", updated_at)

    @dlt.resource(name="discounts", primary_key="id", write_disposition="merge")
    def discounts() -> Iterator[dict[str, Any]]:
        # discountNodes は updated_at 検索フィルタに非対応のため全件洗い替え (merge by id)。
        # discount フィールドをトップに引き上げ、__typename を discount_type として保持する。
        for node in paginate(client, queries.DISCOUNTS, "discountNodes", page_size=page_size):
            discount = node.pop("discount", {}) or {}
            discount_type = discount.pop("__typename", None)
            yield {"id": node.get("id"), "discount_type": discount_type, **discount}

    return orders, customers, products, discounts
