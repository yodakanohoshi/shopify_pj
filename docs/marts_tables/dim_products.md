# marts.dim_products

商品ディメンション。価格レンジ・原価・粗利率・カテゴリ・在庫。粒度: 1 行 = 1 商品。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 商品ID | product_id | varchar | 商品 ID。**PK** |
| 商品レガシーID | product_legacy_id | varchar | 数値 legacy ID |
| 商品名 / URLハンドル | product_title / handle | varchar | 商品名 / ハンドル |
| 商品タイプ / カテゴリ名 / カテゴリ正式名 / ベンダー | product_type / category_name / category_full_name / vendor | varchar | 分類 |
| ステータス | product_status | varchar | ACTIVE / ARCHIVED / DRAFT |
| ギフトカード | is_gift_card | boolean | ギフトカード商品か |
| 在庫追跡有無 | tracks_inventory | boolean | 在庫追跡が有効か |
| 単一既定バリアント | has_only_default_variant | boolean | 既定 1 バリアントのみか |
| バリアント数(API) | variants_count_reported | integer | API 集計のバリアント数 |
| バリアント数 | variant_count | integer | バリアント数 |
| 最低価格 / 最高価格 | min_price / max_price | double | 価格レンジ |
| 平均原価 | avg_unit_cost | double | 平均原価 |
| 粗利率概算 | est_margin_rate | double | 粗利率概算 |
| 総在庫数 | total_inventory | integer | 総在庫 |
| 作成日時 / 公開日時 | created_at / published_at | timestamp | 作成 / 公開日時 |
