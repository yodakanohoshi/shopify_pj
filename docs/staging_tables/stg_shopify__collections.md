# staging.stg_shopify__collections

コレクション。元: `raw.collections`。粒度: 1 行 = 1 コレクション。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| コレクションID | collection_id | varchar | コレクション ID。**PK** |
| コレクション名 / URLハンドル | collection_title / handle | varchar | 名称 / ハンドル |
| コレクション説明 | collection_description | varchar | HTMLタグ除去の説明文 |
| テンプレ接尾辞 | template_suffix | varchar | 表示テーマテンプレの接尾辞 |
| 並び順 | sort_order | varchar | 並び順 |
| SEOタイトル / SEO説明 | seo_title / seo_description | varchar | SEO用タイトル / 説明 |
| 商品数 | products_count | integer | 所属商品数 (API 集計値) |
| 更新日時 | updated_at | timestamp | 更新日時 |
