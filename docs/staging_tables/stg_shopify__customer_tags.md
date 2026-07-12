# staging.stg_shopify__customer_tags

顧客タグ (long 形式)。raw `customers__tags` を raw `customers` と結合し、顧客 gid を
数値 ID へ変換したブリッジ。粒度: 1 行 = (顧客 × タグ)。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 顧客ID | customer_id | varchar | 数値ID (gid から抽出)。**FK → stg_shopify__customers.customer_id** |
| タグ | tag | varchar | タグ文字列 |
