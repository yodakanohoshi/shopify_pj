# raw.product_variants

商品バリアント。取得方式: **Bulk** (`products.variants`)。粒度: 1 行 = 1 バリアント。

| カラム | 型 | 説明 |
|---|---|---|
| id | varchar | バリアント global ID。**PK** |
| parent_id | varchar | 親商品の gid。**FK → products.id** |
| legacy_resource_id | varchar | 数値 legacy ID |
| title / sku / barcode | varchar | 名称 / SKU / バーコード |
| price / compare_at_price | varchar(数値) | 価格 / 参考価格 |
| inventory_item__unit_cost__amount | varchar(数値) | **原価** (粗利計算に使用) |
| inventory_item__unit_cost__currency_code | varchar | 原価通貨 |
| inventory_item__measurement__weight__value / __unit | varchar | 重量 / 単位 |
| inventory_quantity | bigint | 在庫数 |
| position | bigint | 表示順 |
| selected_options | (子: product_variants__selected_options) | 選択オプション (name / value) |
