# staging.stg_shopify__products

商品マスタ。元: `raw.products`。粒度: 1 行 = 1 商品。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 商品ID | product_id | varchar | 商品 ID。**PK** |
| 商品レガシーID | product_legacy_id | varchar | 数値 legacy ID |
| 商品名 / URLハンドル | product_title / handle | varchar | 商品名 / ハンドル |
| 商品説明 | product_description | varchar | HTMLタグ除去の説明文 |
| 商品タイプ / ベンダー | product_type / vendor | varchar | タイプ / ベンダー |
| ステータス | product_status | varchar | ACTIVE / ARCHIVED / DRAFT |
| テンプレ接尾辞 | template_suffix | varchar | 商品表示テーマテンプレの接尾辞 |
| 公開URL | online_store_url | varchar | オンラインストア上のURL |
| ギフトカード | is_gift_card | boolean | ギフトカード商品か |
| 在庫追跡有無 | tracks_inventory | boolean | 在庫追跡が有効か |
| 単一既定バリアント | has_only_default_variant | boolean | 既定1バリアントのみか |
| 販売プラン必須 | requires_selling_plan | boolean | 定期購入のみ購入可か |
| カテゴリID / カテゴリ名 / カテゴリ正式名 | category_id / category_name / category_full_name | varchar | 標準タクソノミのカテゴリ |
| SEOタイトル / SEO説明 | seo_title / seo_description | varchar | SEO用タイトル / 説明 |
| バリアント数(API) | variants_count | integer | API集計のバリアント数 |
| 総在庫数 | total_inventory | integer | 総在庫 |
| 作成日時 / 更新日時 / 公開日時 | created_at / updated_at / published_at | timestamp | 各日時 |
