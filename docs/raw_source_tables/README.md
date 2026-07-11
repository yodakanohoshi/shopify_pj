# raw ソーステーブル (`raw` スキーマ)

dlt が Shopify Admin GraphQL API から投入する生データ。列名 snake_case、ネストは `__` 平坦化。
全テーブルに監査列 `_dlt_id` / `_dlt_load_id` が付く (各ファイルでは省略)。

| テーブル | 取得方式 | 親 | 定義 |
|---|---|---|---|
| orders | Bulk | — | [orders.md](orders.md) |
| order_line_items | Bulk | orders | [order_line_items.md](order_line_items.md) |
| orders__discount_codes | Bulk (inline list) | orders | [orders__discount_codes.md](orders__discount_codes.md) |
| products | Bulk | — | [products.md](products.md) |
| product_variants | Bulk | products | [product_variants.md](product_variants.md) |
| customers | Bulk | — | [customers.md](customers.md) |
| customer_addresses | Bulk | customers | [customer_addresses.md](customer_addresses.md) |
| collections | Bulk | — | [collections.md](collections.md) |
| collection_products | Bulk | collections | [collection_products.md](collection_products.md) |
| abandoned_checkouts | Bulk | — | [abandoned_checkouts.md](abandoned_checkouts.md) |
| abandoned_checkout_line_items | Bulk | abandoned_checkouts | [abandoned_checkout_line_items.md](abandoned_checkout_line_items.md) |
| discounts | ページング | — | [discounts.md](discounts.md) |
| discounts__codes | ページング (子) | discounts | [discounts__codes.md](discounts__codes.md) |
| locations | ページング | — | [locations.md](locations.md) |

## 結合キーの規則

- **Bulk の子テーブル**: `parent_id` (親の gid) = 親テーブルの `id`。
- **inline list の子テーブル** (`*__discount_codes` 等): `_dlt_parent_id` = 親テーブルの `_dlt_id`。
