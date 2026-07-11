# marts.dim_products

商品ディメンション。価格レンジ・原価・粗利率・カテゴリ・在庫。粒度: 1 行 = 1 商品。

| カラム | 型 | 説明 |
|---|---|---|
| product_id | varchar | 商品 ID。**PK** |
| product_legacy_id | varchar | 数値 legacy ID |
| product_title / handle | varchar | 商品名 / ハンドル |
| product_type / category_name / category_full_name / vendor | varchar | 分類 |
| product_status | varchar | ACTIVE / ARCHIVED / DRAFT |
| variant_count | integer | バリアント数 |
| min_price / max_price | double | 価格レンジ |
| avg_unit_cost | double | 平均原価 |
| est_margin_rate | double | 粗利率概算 |
| total_inventory | integer | 総在庫 |
| created_at / published_at | timestamp | 作成 / 公開日時 |
