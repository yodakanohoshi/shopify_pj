# staging.stg_shopify__abandoned_checkout_lines

放棄チェックアウト明細。元: `raw.abandoned_checkout_line_items`。粒度: 1 行 = 1 明細。

| カラム | 型 | 説明 |
|---|---|---|
| checkout_line_id | varchar | 明細 ID。**PK** |
| checkout_id | varchar | 親チェックアウト ID。**FK → stg_shopify__abandoned_checkouts** |
| product_id / variant_id | varchar | 商品 / バリアント ID |
| product_title | varchar | 商品名 |
| quantity | integer | 数量 |
