# intermediate.int_products__enriched

商品 + バリアント集計 (価格レンジ / 平均原価 / 在庫)。粒度: 1 行 = 1 商品。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 商品ID | product_id | varchar | 商品 ID。**PK** |
| 商品レガシーID | product_legacy_id | varchar | legacy ID |
| 商品名 / URLハンドル | product_title / handle | varchar | 商品名 / ハンドル |
| 商品タイプ / カテゴリ名 / カテゴリ正式名 / ベンダー | product_type / category_name / category_full_name / vendor | varchar | 分類 |
| ステータス | product_status | varchar | ステータス |
| バリアント数 | variant_count | integer | バリアント数 |
| 最低価格 / 最高価格 | min_price / max_price | double | 価格レンジ |
| 平均原価 | avg_unit_cost | double | 平均原価 |
| 粗利率概算 | est_margin_rate | double | 粗利率概算 = (min_price − avg_unit_cost) / min_price |
| 総在庫数 | total_inventory | integer | 総在庫 |
| 作成日時 / 公開日時 | created_at / published_at | timestamp | 各日時 |
