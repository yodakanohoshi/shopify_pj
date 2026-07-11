# staging テーブル (`staging` スキーマ)

raw を 1:1 でクレンジング (型付け・リネーム・金額の数値化) した層。dbt materialized: **view**。
命名: `stg_<source>__<entity>`。ビジネスロジックは持たない。

| テーブル | 元 raw | 定義 |
|---|---|---|
| stg_shopify__orders | orders | [stg_shopify__orders.md](stg_shopify__orders.md) |
| stg_shopify__order_lines | order_line_items | [stg_shopify__order_lines.md](stg_shopify__order_lines.md) |
| stg_shopify__order_discount_codes | orders__discount_codes | [stg_shopify__order_discount_codes.md](stg_shopify__order_discount_codes.md) |
| stg_shopify__customers | customers | [stg_shopify__customers.md](stg_shopify__customers.md) |
| stg_shopify__customer_addresses | customer_addresses | [stg_shopify__customer_addresses.md](stg_shopify__customer_addresses.md) |
| stg_shopify__products | products | [stg_shopify__products.md](stg_shopify__products.md) |
| stg_shopify__product_variants | product_variants | [stg_shopify__product_variants.md](stg_shopify__product_variants.md) |
| stg_shopify__collections | collections | [stg_shopify__collections.md](stg_shopify__collections.md) |
| stg_shopify__collection_products | collection_products | [stg_shopify__collection_products.md](stg_shopify__collection_products.md) |
| stg_shopify__abandoned_checkouts | abandoned_checkouts | [stg_shopify__abandoned_checkouts.md](stg_shopify__abandoned_checkouts.md) |
| stg_shopify__abandoned_checkout_lines | abandoned_checkout_line_items | [stg_shopify__abandoned_checkout_lines.md](stg_shopify__abandoned_checkout_lines.md) |
| stg_shopify__discounts | discounts | [stg_shopify__discounts.md](stg_shopify__discounts.md) |
| stg_shopify__discount_codes | discounts__codes | [stg_shopify__discount_codes.md](stg_shopify__discount_codes.md) |
| stg_shopify__locations | locations | [stg_shopify__locations.md](stg_shopify__locations.md) |
