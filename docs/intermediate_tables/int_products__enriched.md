# intermediate.int_products__enriched

商品 + バリアント集計 (価格レンジ / 平均原価 / 在庫)。粒度: 1 行 = 1 商品。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 商品ID | product_id | varchar | 数値ID (gid から抽出)。**PK** |
| 商品レガシーID | product_legacy_id | varchar | legacy ID |
| 商品名 / URLハンドル | product_title / handle | varchar | 商品名 / ハンドル |
| 商品タイプ / カテゴリ名 / カテゴリ正式名 / ベンダー | product_type / category_name / category_full_name / vendor | varchar | 分類 |
| ステータス | product_status | varchar | ステータス |
| 商品説明 | product_description | varchar | HTMLタグ除去の説明文 |
| ギフトカード / 在庫追跡有無 / 単一既定バリアント | is_gift_card / tracks_inventory / has_only_default_variant | boolean | ギフトカード商品か / 在庫追跡有効か / 既定1バリアントのみか |
| バリアント数(API) | variants_count_reported | integer | API集計のバリアント数 |
| バリアント数 | variant_count | integer | バリアント数 |
| 最低価格 / 最高価格 | min_price / max_price | double | 価格レンジ |
| 平均原価 | avg_unit_cost | double | 平均原価 |
| 粗利率概算 | est_margin_rate | double | 粗利率概算 = (min_price − avg_unit_cost) / min_price |
| 総在庫数 | total_inventory | integer | 総在庫 |
| SKU一覧 / JAN一覧 | sku_list / jan_list | varchar | 配下バリアントの SKU / バーコード(JAN等) をカンマ連結 |
| タグ | tags | varchar | 商品タグをカンマ連結 (明細は stg_shopify__product_tags) |
| 作成日時 / 公開日時 | created_at / published_at | timestamp | 各日時 |
