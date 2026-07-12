# raw.products

商品ヘッダ。取得方式: **Bulk** (`products`)。粒度: 1 行 = 1 商品。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 商品ID | id | varchar | 商品 global ID。**PK** |
| 商品レガシーID | legacy_resource_id | varchar | 数値 legacy 商品 ID |
| 商品名 / URLハンドル | title / handle | varchar | 商品名 / URL ハンドル |
| 商品タイプ / ベンダー | product_type / vendor | varchar | 商品タイプ / ベンダー |
| ステータス | status | varchar | ACTIVE / ARCHIVED / DRAFT |
| カテゴリID / カテゴリ名 / カテゴリ正式名 | category__id / category__name / category__full_name | varchar | 標準タクソノミのカテゴリ |
| 総在庫数 | total_inventory | bigint | 総在庫数 |
| タグ | tags | (子: products__tags) | タグ (inline list) |
| 商品オプション | options | (子: products__options) | 商品オプション (name / position) |
| 作成日時 / 更新日時 / 公開日時 | created_at / updated_at / published_at | varchar(ISO8601) | 各日時 |

子テーブル: [product_variants](product_variants.md) (parent_id → id)。
