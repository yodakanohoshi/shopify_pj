# staging.stg_shopify__product_variants

商品バリアント。元: `raw.product_variants`。粒度: 1 行 = 1 バリアント。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| バリアントID | variant_id | varchar | バリアント ID。**PK** |
| バリアントレガシーID | variant_legacy_id | varchar | 数値 legacy ID |
| 商品ID | product_id | varchar | 親商品 ID。**FK → stg_shopify__products.product_id** |
| バリアント名 / 表示名 | variant_title / variant_display_name | varchar | バリアント名 / 商品名+バリアント名 |
| SKU / バーコード | sku / barcode | varchar | SKU・バーコード |
| 価格 / 参考価格 | price / compare_at_price | double | 価格 / 参考価格 |
| 販売可否 | available_for_sale | boolean | 販売可能か |
| 課税対象 | taxable | boolean | 販売時課税されるか |
| 在庫ポリシー | inventory_policy | varchar | 在庫切れ時の注文可否 |
| 在庫アイテムID | inventory_item_id | varchar | 在庫レベルとの結合キー。数値ID (gid から抽出) |
| 在庫追跡 | inventory_tracked | boolean | 在庫レベル追跡有無 |
| 配送要否 | requires_shipping | boolean | 配送が必要か |
| 原価 / 通貨コード | unit_cost / unit_cost_currency | double / varchar | **原価** / 通貨 (粗利計算) |
| 重量 / 重量単位 | weight_value / weight_unit | double / varchar | 重量 / 単位 |
| 在庫数 | inventory_quantity | integer | 在庫数 |
| オンライン販売可能数 | sellable_online_quantity | integer | オンライン向け販売可能数 |
| 表示順 | position | integer | 表示順 |
| 作成日時 / 更新日時 | created_at / updated_at | timestamp | 各日時 |
