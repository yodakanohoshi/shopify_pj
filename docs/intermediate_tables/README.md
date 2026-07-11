# intermediate テーブル (`intermediate` スキーマ)

staging を結合・集計した中間表現。dbt materialized: **view**。命名: `int_<entity>__<verb>`。
marts の素地であり、原則 BI から直接参照しない。

| テーブル | 定義 |
|---|---|
| int_orders__enriched | [int_orders__enriched.md](int_orders__enriched.md) |
| int_order_lines__enriched | [int_order_lines__enriched.md](int_order_lines__enriched.md) |
| int_products__enriched | [int_products__enriched.md](int_products__enriched.md) |
| int_customers__enriched | [int_customers__enriched.md](int_customers__enriched.md) |
| int_discounts__enriched | [int_discounts__enriched.md](int_discounts__enriched.md) |
| int_product_collections | [int_product_collections.md](int_product_collections.md) |
| int_abandoned_checkouts__enriched | [int_abandoned_checkouts__enriched.md](int_abandoned_checkouts__enriched.md) |
