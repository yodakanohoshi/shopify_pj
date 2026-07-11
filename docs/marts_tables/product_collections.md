# marts.product_collections

商品×コレクションのブリッジ。カテゴリ別売上ロールアップに使う。
粒度: 1 行 = (コレクション × 商品)。

| カラム | 型 | 説明 |
|---|---|---|
| collection_id | varchar | コレクション ID。**FK → dim_collections** |
| collection_title / collection_handle | varchar | コレクション名 / ハンドル |
| product_id | varchar | 商品 ID。**FK → dim_products** |
| product_title / product_type | varchar | 商品名 / タイプ |
