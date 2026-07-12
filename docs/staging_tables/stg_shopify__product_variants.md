# staging.stg_shopify__product_variants

商品バリアント。元: `raw.product_variants`。粒度: 1 行 = 1 バリアント。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| バリアントID | variant_id | varchar | バリアント ID。**PK** |
| バリアントレガシーID | variant_legacy_id | varchar | 数値 legacy ID |
| 商品ID | product_id | varchar | 親商品 ID。**FK → stg_shopify__products.product_id** |
| バリアント名 / SKU / バーコード | variant_title / sku / barcode | varchar | 名称・SKU・バーコード |
| 価格 / 参考価格 | price / compare_at_price | double | 価格 / 参考価格 |
| 原価 / 通貨コード | unit_cost / unit_cost_currency | double / varchar | **原価** / 通貨 (粗利計算) |
| 重量 / 重量単位 | weight_value / weight_unit | double / varchar | 重量 / 単位 |
| 在庫数 | inventory_quantity | integer | 在庫数 |
| 表示順 | position | integer | 表示順 |
