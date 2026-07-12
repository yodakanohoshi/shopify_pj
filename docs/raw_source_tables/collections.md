# raw.collections

コレクション。取得方式: **Bulk** (`collections`)。粒度: 1 行 = 1 コレクション。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| コレクションID | id | varchar | コレクション global ID。**PK** |
| コレクション名 / URLハンドル | title / handle | varchar | 名称 / ハンドル |
| 説明(プレーン) | description | varchar | HTML タグ除去の説明文 |
| テンプレ接尾辞 | template_suffix | varchar | 表示テーマテンプレの接尾辞 |
| 並び順 | sort_order | varchar | 並び順 (MANUAL, BEST_SELLING 等) |
| 商品数 | products_count__count | bigint | 所属商品数 (API 集計値) |
| SEOタイトル / SEO説明 | seo__title / seo__description | varchar | SEO 用タイトル / 説明 |
| 更新日時 | updated_at | varchar(ISO8601) | 更新日時 |

子テーブル: [collection_products](collection_products.md) (parent_id → id)。
