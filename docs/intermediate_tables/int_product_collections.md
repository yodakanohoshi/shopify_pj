# intermediate.int_product_collections

商品×コレクションのブリッジ (名称付与)。粒度: 1 行 = (コレクション × 商品)。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| コレクションID | collection_id | varchar | 数値ID (gid から抽出) |
| コレクション名 / URLハンドル | collection_title / collection_handle | varchar | コレクション名 / ハンドル |
| 商品ID | product_id | varchar | 数値ID (gid から抽出) |
| 商品名 / 商品タイプ | product_title / product_type | varchar | 商品名 / タイプ |
