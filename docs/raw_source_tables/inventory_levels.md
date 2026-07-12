# raw.inventory_levels

ロケーション×在庫アイテムの在庫スナップショット。取得方式: **Bulk** (`locations.inventoryLevels`)。
書き込み: **replace** (毎回全件洗い替え)。粒度: 1 行 = (ロケーション × 在庫アイテム)。

> InventoryLevel ノードは `__parentId` にロケーション gid を持ち、`item__id` で
> `product_variants.inventory_item__id` と結合できる。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 在庫レベルID | id | varchar | InventoryLevel global ID。**PK** |
| 親ID(ロケーション) | parent_id | varchar | 親ロケーションの gid。**FK → locations.id** |
| 在庫アイテムID | item__id | varchar | InventoryItem gid (variant の inventory_item__id と結合) |
| SKU | item__sku | varchar | 在庫アイテムの SKU |
| 数量群 | quantities | (子: inventory_levels__quantities) | name / quantity ペア (inline list) |

子テーブル: [inventory_levels__quantities](inventory_levels__quantities.md) (_dlt_parent_id → _dlt_id)。
