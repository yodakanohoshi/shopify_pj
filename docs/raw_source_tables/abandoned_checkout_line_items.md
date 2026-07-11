# raw.abandoned_checkout_line_items

放棄チェックアウトの明細。取得方式: **Bulk** (`abandonedCheckouts.lineItems`)。
粒度: 1 行 = 1 明細。

| カラム | 型 | 説明 |
|---|---|---|
| id | varchar | 明細 global ID。**PK** |
| parent_id | varchar | 親チェックアウトの gid。**FK → abandoned_checkouts.id** |
| title | varchar | 商品名 |
| quantity | bigint | 数量 |
| product__id / variant__id | varchar | 商品 / バリアント ID |
