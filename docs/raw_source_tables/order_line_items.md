# raw.order_line_items

注文明細。取得方式: **Bulk** (`orders.lineItems`)。粒度: 1 行 = 1 明細。

| カラム | 型 | 説明 |
|---|---|---|
| id | varchar | 明細 global ID。**PK** |
| parent_id | varchar | 親注文の gid。**FK → orders.id** |
| title | varchar | 商品名 (注文時点) |
| quantity | bigint | 数量 |
| sku / vendor | varchar | SKU / ベンダー |
| product__id | varchar | 商品 ID (FK → products.id) |
| variant__id | varchar | バリアント ID (FK → product_variants.id) |
| original_unit_price_set__shop_money__amount | varchar(数値) | 元単価 |
| discounted_unit_price_set__shop_money__amount | varchar(数値) | 割引後単価 |
| total_discount_set__shop_money__amount | varchar(数値) | 明細割引額 |
