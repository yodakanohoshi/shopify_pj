# staging.stg_shopify__products

商品マスタ。元: `raw.products`。粒度: 1 行 = 1 商品。

| カラム | 型 | 説明 |
|---|---|---|
| product_id | varchar | 商品 ID。**PK** |
| product_legacy_id | varchar | 数値 legacy ID |
| product_title / handle | varchar | 商品名 / ハンドル |
| product_type / vendor | varchar | タイプ / ベンダー |
| product_status | varchar | ACTIVE / ARCHIVED / DRAFT |
| category_id / category_name / category_full_name | varchar | 標準タクソノミのカテゴリ |
| total_inventory | integer | 総在庫 |
| created_at / updated_at / published_at | timestamp | 各日時 |
