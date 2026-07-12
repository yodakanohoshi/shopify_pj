# raw.product_variants

商品バリアント。取得方式: **Bulk** (`products.variants`)。粒度: 1 行 = 1 バリアント。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| バリアントID | id | varchar | バリアント global ID。**PK** |
| 親ID | parent_id | varchar | 親商品の gid。**FK → products.id** |
| レガシーID | legacy_resource_id | varchar | 数値 legacy ID |
| バリアント名 / SKU / バーコード | title / sku / barcode | varchar | 名称 / SKU / バーコード |
| 表示名 | display_name | varchar | 商品名 + バリアント名 |
| 価格 / 参考価格 | price / compare_at_price | varchar(数値) | 価格 / 参考価格 |
| 販売可否 | available_for_sale | boolean | 販売可能か |
| 課税対象 | taxable | boolean | 販売時課税されるか |
| 在庫ポリシー | inventory_policy | varchar | 在庫切れ時の注文可否 |
| 在庫アイテムID | inventory_item__id | varchar | 在庫レベルとの結合キー (gid) |
| 在庫追跡 | inventory_item__tracked | boolean | 在庫レベル追跡有無 |
| 配送要否 | inventory_item__requires_shipping | boolean | 配送が必要か |
| 原価 | inventory_item__unit_cost__amount | varchar(数値) | **原価** (粗利計算に使用) |
| 原価通貨 | inventory_item__unit_cost__currency_code | varchar | 原価通貨 |
| 重量 / 重量単位 | inventory_item__measurement__weight__value / __unit | varchar | 重量 / 単位 |
| 在庫数 | inventory_quantity | bigint | 在庫数 |
| オンライン販売可能数 | sellable_online_quantity | varchar(数値) | オンライン向け販売可能数 |
| 表示順 | position | bigint | 表示順 |
| 選択オプション | selected_options | (子: product_variants__selected_options) | 選択オプション (name / value) |
| 作成日時 / 更新日時 | created_at / updated_at | varchar(ISO8601) | バリアント作成 / 最終更新日時 |
