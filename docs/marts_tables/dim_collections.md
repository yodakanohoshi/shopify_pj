# marts.dim_collections

コレクションディメンション。粒度: 1 行 = 1 コレクション。

| カラム | 型 | 説明 |
|---|---|---|
| collection_id | varchar | コレクション ID。**PK** |
| collection_title / handle | varchar | 名称 / ハンドル |
| sort_order | varchar | 並び順 |
| products_count_reported | integer | 所属商品数 (API 集計値) |
| products_count_actual | integer | 所属商品数 (ブリッジ実測) |
| updated_at | timestamp | 更新日時 |
