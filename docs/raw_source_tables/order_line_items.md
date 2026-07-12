# raw.order_line_items

注文明細。取得方式: **Bulk** (`orders.lineItems`)。粒度: 1 行 = 1 明細。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 明細ID | id | varchar | 明細 global ID。**PK** |
| 親ID | parent_id | varchar | 親注文の gid。**FK → orders.id** |
| 商品名 | title | varchar | 商品名 (注文時点) |
| 数量 | quantity | bigint | 数量 |
| SKU / ベンダー | sku / vendor | varchar | SKU / ベンダー |
| 商品ID | product__id | varchar | 商品 ID (FK → products.id) |
| バリアントID | variant__id | varchar | バリアント ID (FK → product_variants.id) |
| 単価(定価) | original_unit_price_set__shop_money__amount | varchar(数値) | 元単価 |
| 割引後単価 | discounted_unit_price_set__shop_money__amount | varchar(数値) | 割引後単価 |
| 明細割引額 | total_discount_set__shop_money__amount | varchar(数値) | 明細割引額 |
