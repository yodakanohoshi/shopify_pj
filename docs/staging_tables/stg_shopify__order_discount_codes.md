# staging.stg_shopify__order_discount_codes

注文に適用された割引コード。元: `raw.orders__discount_codes`。粒度: 1 行 = (注文 × コード)。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 注文dlt行ID | order_dlt_id | varchar | 親注文の dlt 行 ID。**FK → stg_shopify__orders.order_dlt_id** |
| 割引コード | discount_code | varchar | 割引コード文字列 |
