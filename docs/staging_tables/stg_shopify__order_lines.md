# staging.stg_shopify__order_lines

注文明細。元: `raw.order_line_items`。粒度: 1 行 = 1 明細。

| カラム | 型 | 説明 |
|---|---|---|
| order_line_id | varchar | 明細 ID。**PK** |
| order_id | varchar | 親注文 ID。**FK → stg_shopify__orders.order_id** |
| product_id / variant_id | varchar | 商品 / バリアント ID |
| product_title | varchar | 注文時点の商品名 |
| sku / vendor | varchar | SKU / ベンダー |
| quantity | integer | 数量 |
| original_unit_price / discounted_unit_price / line_discount | double | 元単価 / 割引後単価 / 明細割引 |
