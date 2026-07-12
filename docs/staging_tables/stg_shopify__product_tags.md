# staging.stg_shopify__product_tags

商品タグ (long 形式)。raw `products__tags` を raw `products` と結合し、商品 gid を
数値 ID へ変換したブリッジ。粒度: 1 行 = (商品 × タグ)。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 商品ID | product_id | varchar | 数値ID (gid から抽出)。**FK → stg_shopify__products.product_id** |
| タグ | tag | varchar | タグ文字列 |
