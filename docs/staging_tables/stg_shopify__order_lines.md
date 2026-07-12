# staging.stg_shopify__order_lines

注文明細。元: `raw.order_line_items`。粒度: 1 行 = 1 明細。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 明細ID | order_line_id | varchar | 明細 ID。**PK** |
| 注文ID | order_id | varchar | 親注文 ID。**FK → stg_shopify__orders.order_id** |
| 商品ID / バリアントID | product_id / variant_id | varchar | 商品 / バリアント ID |
| 商品名 | product_title | varchar | 注文時点の商品名 |
| SKU / ベンダー | sku / vendor | varchar | SKU / ベンダー |
| 数量 | quantity | integer | 数量 |
| 単価(定価) / 割引後単価 / 明細割引額 | original_unit_price / discounted_unit_price / line_discount | double | 元単価 / 割引後単価 / 明細割引 |
