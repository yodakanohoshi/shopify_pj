"""Shopify Admin GraphQL を対象とした dlt ソース。

分析に有用なオブジェクトを幅広く取得する。大きくネストするソース
(orders / products / customers / collections / abandoned_checkouts) は
**Bulk Operations** で全件エクスポートし、JSONL を型ごとのテーブルへ振り分ける。
件数が少ない/Bulk に載せにくいソース (discounts / locations) は通常ページング。

dlt 標準ソースが非対応でも、分析に有用なら discounts と同様にカスタム取得する。

書き込みは全リソース replace (Bulk は全件エクスポートのため全面洗い替え)。
"""

from __future__ import annotations

from typing import Any, Iterable, Iterator

import dlt
from dlt.sources import DltResource

from . import queries
from .bulk import route_records, run_bulk
from .helpers import ShopifyGraphQLClient, paginate

# Bulk JSONL の gid 型 → 出力テーブル名 (リソースごと)
ORDER_TYPES = {"Order": "orders", "LineItem": "order_line_items"}
PRODUCT_TYPES = {"Product": "products", "ProductVariant": "product_variants"}
CUSTOMER_TYPES = {"Customer": "customers", "MailingAddress": "customer_addresses"}
COLLECTION_TYPES = {"Collection": "collections", "Product": "collection_products"}
CHECKOUT_TYPES = {
    "AbandonedCheckout": "abandoned_checkouts",
    "AbandonedCheckoutLineItem": "abandoned_checkout_line_items",
}


@dlt.source(name="shopify")
def shopify_source(
    shop: str = dlt.config.value,
    access_token: str | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
    api_version: str = "2025-01",
    page_size: int = 100,
) -> Iterable[DltResource]:
    """Shopify の主要オブジェクトを raw スキーマへ幅広くロードするソース。

    認証は client_id + client_secret (Client Credentials Grant) か access_token の
    いずれか。dlt が config/secrets/環境変数から注入する。
    """

    client = ShopifyGraphQLClient(
        shop=shop,
        api_version=api_version,
        access_token=access_token,
        client_id=client_id,
        client_secret=client_secret,
    )

    def _bulk_resource(query: str, type_map: dict[str, str]) -> Iterator[Any]:
        """Bulk を実行し、各レコードを型に応じたテーブル名へ振り分けて yield する。"""
        for table, record in route_records(run_bulk(client, query), type_map):
            yield dlt.mark.with_table_name(record, table)

    @dlt.resource(name="orders", write_disposition="replace")
    def orders() -> Iterator[Any]:
        yield from _bulk_resource(queries.BULK_ORDERS, ORDER_TYPES)

    @dlt.resource(name="products", write_disposition="replace")
    def products() -> Iterator[Any]:
        yield from _bulk_resource(queries.BULK_PRODUCTS, PRODUCT_TYPES)

    @dlt.resource(name="customers", write_disposition="replace")
    def customers() -> Iterator[Any]:
        yield from _bulk_resource(queries.BULK_CUSTOMERS, CUSTOMER_TYPES)

    @dlt.resource(name="collections", write_disposition="replace")
    def collections() -> Iterator[Any]:
        yield from _bulk_resource(queries.BULK_COLLECTIONS, COLLECTION_TYPES)

    @dlt.resource(name="abandoned_checkouts", write_disposition="replace")
    def abandoned_checkouts() -> Iterator[Any]:
        yield from _bulk_resource(queries.BULK_ABANDONED_CHECKOUTS, CHECKOUT_TYPES)

    @dlt.resource(name="discounts", primary_key="id", write_disposition="replace")
    def discounts() -> Iterator[dict[str, Any]]:
        # discount フィールドをトップに引き上げ、__typename を discount_type として保持。
        for node in paginate(client, queries.DISCOUNTS_PAGINATED, "discountNodes", page_size=page_size):
            discount = node.pop("discount", {}) or {}
            discount_type = discount.pop("__typename", None)
            yield {"id": node.get("id"), "discount_type": discount_type, **discount}

    @dlt.resource(name="locations", primary_key="id", write_disposition="replace")
    def locations() -> Iterator[dict[str, Any]]:
        yield from paginate(client, queries.LOCATIONS_PAGINATED, "locations", page_size=page_size)

    return (
        orders,
        products,
        customers,
        collections,
        abandoned_checkouts,
        discounts,
        locations,
    )
