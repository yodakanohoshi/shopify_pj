# staging.stg_shopify__abandoned_checkout_lines

放棄チェックアウト明細。元: `raw.abandoned_checkout_line_items`。粒度: 1 行 = 1 明細。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 明細ID | checkout_line_id | varchar | 明細 ID。**PK** |
| カゴ落ちID | checkout_id | varchar | 親チェックアウト ID。**FK → stg_shopify__abandoned_checkouts** |
| 商品ID / バリアントID | product_id / variant_id | varchar | 商品 / バリアント ID |
| 商品名 | product_title | varchar | 商品名 |
| 数量 | quantity | integer | 数量 |
