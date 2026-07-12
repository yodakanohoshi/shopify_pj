# marts.fct_inventory_levels

在庫レベルファクト。欠品・在庫回転の分析基点。在庫アイテムをバリアント/商品に、ロケーションを拠点に紐づける。粒度: 1 行 = (ロケーション × 在庫アイテム) の在庫スナップショット。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 在庫レベルID | inventory_level_id | varchar | InventoryLevel ID。**PK** |
| ロケーションID | location_id | varchar | 数値ID (gid から抽出)。**FK → dim_locations** |
| ロケーション名 | location_name | varchar | 拠点名 |
| 在庫アイテムID | inventory_item_id | varchar | 数値ID (gid から抽出。variant の inventory_item_id と結合) |
| バリアントID / 商品ID | variant_id / product_id | varchar | 数値ID (gid から抽出)。**FK → dim_products** |
| SKU | sku | varchar | 在庫アイテムの SKU |
| 利用可能数 | available | integer | 販売可能な在庫数 |
| 実在庫数 | on_hand | integer | 物理的に保有する在庫数 |
| 引当数 | committed | integer | 注文で引き当て済みの数 |
| 入荷予定数 | incoming | integer | 入荷予定の数 |
