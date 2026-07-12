# marts.dim_collections

コレクションディメンション。粒度: 1 行 = 1 コレクション。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| コレクションID | collection_id | varchar | コレクション ID。**PK** |
| コレクション名 / URLハンドル | collection_title / handle | varchar | 名称 / ハンドル |
| 並び順 | sort_order | varchar | 並び順 |
| 商品数(API集計) | products_count_reported | integer | 所属商品数 (API 集計値) |
| 商品数(実測) | products_count_actual | integer | 所属商品数 (ブリッジ実測) |
| 更新日時 | updated_at | timestamp | 更新日時 |
