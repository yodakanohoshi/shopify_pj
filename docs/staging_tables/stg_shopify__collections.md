# staging.stg_shopify__collections

コレクション。元: `raw.collections`。粒度: 1 行 = 1 コレクション。

| カラム | 型 | 説明 |
|---|---|---|
| collection_id | varchar | コレクション ID。**PK** |
| collection_title / handle | varchar | 名称 / ハンドル |
| sort_order | varchar | 並び順 |
| products_count | integer | 所属商品数 (API 集計値) |
| updated_at | timestamp | 更新日時 |
