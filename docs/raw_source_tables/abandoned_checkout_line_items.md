# raw.abandoned_checkout_line_items

放棄チェックアウトの明細。取得方式: **Bulk** (`abandonedCheckouts.lineItems`)。
粒度: 1 行 = 1 明細。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 明細ID | id | varchar | 明細 global ID。**PK** |
| 親ID | parent_id | varchar | 親チェックアウトの gid。**FK → abandoned_checkouts.id** |
| 商品名 | title | varchar | 商品名 |
| 数量 | quantity | bigint | 数量 |
| 商品ID / バリアントID | product__id / variant__id | varchar | 商品 / バリアント ID |
