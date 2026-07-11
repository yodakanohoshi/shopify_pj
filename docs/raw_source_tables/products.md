# raw.products

商品ヘッダ。取得方式: **Bulk** (`products`)。粒度: 1 行 = 1 商品。

| カラム | 型 | 説明 |
|---|---|---|
| id | varchar | 商品 global ID。**PK** |
| legacy_resource_id | varchar | 数値 legacy 商品 ID |
| title / handle | varchar | 商品名 / URL ハンドル |
| product_type / vendor | varchar | 商品タイプ / ベンダー |
| status | varchar | ACTIVE / ARCHIVED / DRAFT |
| category__id / category__name / category__full_name | varchar | 標準タクソノミのカテゴリ |
| total_inventory | bigint | 総在庫数 |
| tags | (子: products__tags) | タグ (inline list) |
| options | (子: products__options) | 商品オプション (name / position) |
| created_at / updated_at / published_at | varchar(ISO8601) | 各日時 |

子テーブル: [product_variants](product_variants.md) (parent_id → id)。
