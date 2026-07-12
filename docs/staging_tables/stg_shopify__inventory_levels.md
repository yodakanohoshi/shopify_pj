# staging.stg_shopify__inventory_levels

ロケーション×在庫アイテムの在庫スナップショット。元: `raw.inventory_levels` + `raw.inventory_levels__quantities` (name/quantity ペアを name ごとに横持ち集計)。粒度: 1 行 = (ロケーション × 在庫アイテム)。location_id で `stg_shopify__locations.location_id`、inventory_item_id で `stg_shopify__product_variants.inventory_item_id` に紐づく。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 在庫レベルID | inventory_level_id | varchar | InventoryLevel global ID。**PK** |
| ロケーションID | location_id | varchar | ロケーション gid。**FK → stg_shopify__locations.location_id** |
| 在庫アイテムID | inventory_item_id | varchar | InventoryItem gid。**FK → stg_shopify__product_variants.inventory_item_id** |
| SKU | sku | varchar | 在庫アイテムの SKU |
| 利用可能数 | available | integer | 販売可能な在庫数 (name=available) |
| 実在庫数 | on_hand | integer | 物理的な在庫数 (name=on_hand) |
| 引当数 | committed | integer | 注文で引き当て済みの在庫数 (name=committed) |
| 入荷予定数 | incoming | integer | 入荷予定の在庫数 (name=incoming) |
