# staging.stg_shopify__products

商品マスタ。元: `raw.products`。粒度: 1 行 = 1 商品。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 商品ID | product_id | varchar | 商品 ID。**PK** |
| 商品レガシーID | product_legacy_id | varchar | 数値 legacy ID |
| 商品名 / URLハンドル | product_title / handle | varchar | 商品名 / ハンドル |
| 商品タイプ / ベンダー | product_type / vendor | varchar | タイプ / ベンダー |
| ステータス | product_status | varchar | ACTIVE / ARCHIVED / DRAFT |
| カテゴリID / カテゴリ名 / カテゴリ正式名 | category_id / category_name / category_full_name | varchar | 標準タクソノミのカテゴリ |
| 総在庫数 | total_inventory | integer | 総在庫 |
| 作成日時 / 更新日時 / 公開日時 | created_at / updated_at / published_at | timestamp | 各日時 |
