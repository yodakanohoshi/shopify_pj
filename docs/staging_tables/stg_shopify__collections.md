# staging.stg_shopify__collections

コレクション。元: `raw.collections`。粒度: 1 行 = 1 コレクション。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| コレクションID | collection_id | varchar | コレクション ID。**PK** |
| コレクション名 / URLハンドル | collection_title / handle | varchar | 名称 / ハンドル |
| 並び順 | sort_order | varchar | 並び順 |
| 商品数 | products_count | integer | 所属商品数 (API 集計値) |
| 更新日時 | updated_at | timestamp | 更新日時 |
