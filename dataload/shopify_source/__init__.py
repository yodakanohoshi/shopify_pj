"""Shopify Admin GraphQL を対象とした dlt ソース。

分析に有用なオブジェクトを幅広く取得する。大きくネストするソース
(orders / products / customers / collections / abandoned_checkouts) は
**Bulk Operations** で全件エクスポートし、JSONL を型ごとのテーブルへ振り分ける。
件数が少ない/Bulk に載せにくいソース (discounts / locations) は通常ページング。

## 取得モード

想定する運用は次の2つ:

- **差分取得 (既定)**: 日次/毎時のスケジュール実行。前回実行で記録した高水位
  (``updated_at`` / ``created_at``) 以降だけを Shopify 側の検索フィルタで絞って
  取得し、``merge`` で upsert する。**Bulk も差分**で、connection の
  ``(query: "updated_at:>=...")`` を注入して更新分だけをエクスポートする。
  初回実行は高水位が無いため自動的に全件取得 (=初回バックフィル) となる。
- **バックフィル (手動・随時)**: 過去分をまとめて取り直したいときに ``backfill=True``
  または ``start_date`` / ``end_date`` で期間を指定して呼ぶ。保存済み高水位を無視して
  対象期間を再取得する。高水位は前進のみ (過去窓の再取得で巻き戻さない)。

大きく変動しない小さなディメンション (discounts / locations) は差分に載せず、
毎回 ``replace`` で全件洗い替えする (件数が少なく安全側)。
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

# Bulk リソースの差分取得定義:
#   (リソース名, Bulk テンプレート, 型→テーブル対応,
#    Shopify 検索フィールド, 親ノードの高水位フィールド)
# 高水位フィールドは親ノードのみが持ち (子ノードは持たない)、状態の前進に使う。
BULK_RESOURCES = [
    ("orders", queries.BULK_ORDERS, ORDER_TYPES, "updated_at", "updatedAt"),
    ("products", queries.BULK_PRODUCTS, PRODUCT_TYPES, "updated_at", "updatedAt"),
    ("customers", queries.BULK_CUSTOMERS, CUSTOMER_TYPES, "updated_at", "updatedAt"),
    ("collections", queries.BULK_COLLECTIONS, COLLECTION_TYPES, "updated_at", "updatedAt"),
    # 放棄チェックアウトは確定後ほぼ不変。created_at を高水位に使う。
    ("abandoned_checkouts", queries.BULK_ABANDONED_CHECKOUTS, CHECKOUT_TYPES, "created_at", "createdAt"),
]


@dlt.source(name="shopify")
def shopify_source(
    shop: str = dlt.config.value,
    access_token: str | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
    api_version: str = "2025-01",
    page_size: int = 100,
    start_date: str | None = None,
    end_date: str | None = None,
    backfill: bool = False,
) -> Iterable[DltResource]:
    """Shopify の主要オブジェクトを raw スキーマへ幅広くロードするソース。

    認証は client_id + client_secret (Client Credentials Grant) か access_token の
    いずれか。dlt が config/secrets/環境変数から注入する。

    差分取得とバックフィルの切り替え:

    - 既定 (``start_date`` / ``end_date`` を渡さず ``backfill=False``): 差分取得。
      各 Bulk リソースは前回の高水位以降のみを取得し ``merge`` で upsert する。
    - ``backfill=True``: 保存済み高水位を無視して全期間を再取得する。
    - ``start_date`` / ``end_date`` (ISO8601 例 ``"2025-01-01"``): 期間を指定した
      バックフィル。片方だけでも可 (下限のみ / 上限のみ)。

    ``start_date`` を渡した場合は ``backfill`` 指定に関わらずバックフィル扱いとなる。
    """

    client = ShopifyGraphQLClient(
        shop=shop,
        api_version=api_version,
        access_token=access_token,
        client_id=client_id,
        client_secret=client_secret,
    )

    # start_date 明示 or backfill フラグ → バックフィル (保存済み高水位を無視)
    manual = backfill or start_date is not None

    def _bulk_resource(
        name: str,
        template: str,
        type_map: dict[str, str],
        filter_field: str,
        cursor_field: str,
    ) -> DltResource:
        """1つの Bulk リソースを、差分/バックフィルどちらでも動く形で生成する。"""

        @dlt.resource(name=name, primary_key="id", write_disposition="merge")
        def resource() -> Iterator[Any]:
            state = dlt.current.resource_state()
            # 差分取得: 保存済み高水位を下限に。バックフィル: start_date を下限に (None=全件)。
            low = start_date if manual else state.get("cursor")
            filter_clause = queries.date_filter(filter_field, low, end_date)
            query = queries.build(template, filter_clause)

            cursor = state.get("cursor")  # 高水位は前進のみ (max)
            for table, record in route_records(run_bulk(client, query), type_map):
                value = record.get(cursor_field)
                if value and (cursor is None or value > cursor):
                    cursor = value
                yield dlt.mark.with_table_name(record, table)
            if cursor is not None:
                state["cursor"] = cursor

        return resource

    bulk_resources = [_bulk_resource(*spec) for spec in BULK_RESOURCES]

    # --- 小さなディメンション: 差分に載せず毎回全件洗い替え ---------------
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

    return (*bulk_resources, discounts, locations)
