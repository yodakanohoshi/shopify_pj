# raw.products

商品ヘッダ。取得方式: **Bulk** (`products`)。粒度: 1 行 = 1 商品。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 商品ID | id | varchar | 商品 global ID。**PK** |
| 商品レガシーID | legacy_resource_id | varchar | 数値 legacy 商品 ID |
| 商品名 / URLハンドル | title / handle | varchar | 商品名 / URL ハンドル |
| 説明(プレーン) | description | varchar | HTML タグ除去の説明文 |
| 商品タイプ / ベンダー | product_type / vendor | varchar | 商品タイプ / ベンダー |
| ステータス | status | varchar | ACTIVE / ARCHIVED / DRAFT |
| ギフトカード | is_gift_card | boolean | ギフトカード商品か |
| 在庫追跡有無 | tracks_inventory | boolean | 在庫追跡が有効か |
| 単一既定バリアント | has_only_default_variant | boolean | 既定1バリアントのみか |
| 販売プラン必須 | requires_selling_plan | boolean | 定期購入のみ購入可か |
| テンプレ接尾辞 | template_suffix | varchar | 商品表示テーマテンプレの接尾辞 |
| 公開URL | online_store_url | varchar | オンラインストア上の URL |
| カテゴリID / カテゴリ名 / カテゴリ正式名 | category__id / category__name / category__full_name | varchar | 標準タクソノミのカテゴリ |
| 総在庫数 | total_inventory | bigint | 総在庫数 |
| バリアント数(API) | variants_count__count | varchar(数値) | API 集計のバリアント数 |
| SEOタイトル / SEO説明 | seo__title / seo__description | varchar | SEO 用タイトル / 説明 |
| タグ | tags | (子: products__tags) | タグ (inline list) |
| 商品オプション | options | (子: products__options) | 商品オプション (name / position) |
| 作成日時 / 更新日時 / 公開日時 | created_at / updated_at / published_at | varchar(ISO8601) | 各日時 |

子テーブル: [product_variants](product_variants.md) (parent_id → id)。
