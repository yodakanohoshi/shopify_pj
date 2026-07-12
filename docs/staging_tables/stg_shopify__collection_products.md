# staging.stg_shopify__collection_products

コレクション所属商品のブリッジ。元: `raw.collection_products`。
粒度: 1 行 = (コレクション × 商品)。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| コレクションID | collection_id | varchar | コレクション ID。**FK → stg_shopify__collections** |
| 商品ID | product_id | varchar | 商品 ID。**FK → stg_shopify__products** |
