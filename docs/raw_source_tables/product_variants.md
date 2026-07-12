# raw.product_variants

商品バリアント。取得方式: **Bulk** (`products.variants`)。粒度: 1 行 = 1 バリアント。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| バリアントID | id | varchar | バリアント global ID。**PK** |
| 親ID | parent_id | varchar | 親商品の gid。**FK → products.id** |
| レガシーID | legacy_resource_id | varchar | 数値 legacy ID |
| バリアント名 / SKU / バーコード | title / sku / barcode | varchar | 名称 / SKU / バーコード |
| 価格 / 参考価格 | price / compare_at_price | varchar(数値) | 価格 / 参考価格 |
| 原価 | inventory_item__unit_cost__amount | varchar(数値) | **原価** (粗利計算に使用) |
| 原価通貨 | inventory_item__unit_cost__currency_code | varchar | 原価通貨 |
| 重量 / 重量単位 | inventory_item__measurement__weight__value / __unit | varchar | 重量 / 単位 |
| 在庫数 | inventory_quantity | bigint | 在庫数 |
| 表示順 | position | bigint | 表示順 |
| 選択オプション | selected_options | (子: product_variants__selected_options) | 選択オプション (name / value) |
