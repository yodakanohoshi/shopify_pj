# staging.stg_shopify__product_variants

商品バリアント。元: `raw.product_variants`。粒度: 1 行 = 1 バリアント。

| カラム | 型 | 説明 |
|---|---|---|
| variant_id | varchar | バリアント ID。**PK** |
| variant_legacy_id | varchar | 数値 legacy ID |
| product_id | varchar | 親商品 ID。**FK → stg_shopify__products.product_id** |
| variant_title / sku / barcode | varchar | 名称・SKU・バーコード |
| price / compare_at_price | double | 価格 / 参考価格 |
| unit_cost / unit_cost_currency | double / varchar | **原価** / 通貨 (粗利計算) |
| weight_value / weight_unit | double / varchar | 重量 / 単位 |
| inventory_quantity | integer | 在庫数 |
| position | integer | 表示順 |
