# docs — テーブル定義書

Shopify 分析基盤の全レイヤのテーブル定義。データは以下の流れで変換される。

```
Shopify Admin GraphQL API
   │  dataload/ (dlt)
   ▼
raw          ← 01-raw-source-tables.md
   │  elt/ (dbt)
   ▼
staging      ← 02-staging-tables.md
   ▼
intermediate ← 03-intermediate-tables.md
   ▼
marts        ← 04-marts-tables.md   ← BI / 分析はここを参照
```

| # | ドキュメント | スキーマ | 生成 | 内容 |
|---|---|---|---|---|
| 01 | [raw ソーステーブル](01-raw-source-tables.md) | `raw` | dlt | API から投入した生データ (子テーブル含む) |
| 02 | [staging テーブル](02-staging-tables.md) | `staging` | dbt (view) | クレンジング・型付け・リネーム済み |
| 03 | [intermediate テーブル](03-intermediate-tables.md) | `intermediate` | dbt (view) | 結合・集計の中間表現 |
| 04 | [marts テーブル](04-marts-tables.md) | `marts` | dbt (table) | 分析・BI 向け最終形 (dim / fct) |

## 記法

- **型** は DuckDB / dbt 上の論理型。金額は Shopify API では文字列で返るため staging 以降で `double` に変換する。
- **PK** = 主キー、**FK** = 外部キー。
- 割引 (discounts) は dlt 標準ソース非対応のため、GraphQL `discountNodes` からカスタム取得している。
- ID は原則 Shopify の GraphQL global ID (`gid://shopify/<Type>/<n>`)。数値の legacy ID は `*_legacy_id` に併記。

## 補足: dlt の正規化規則

- ネストした**単一オブジェクト**は親テーブルに `親__子__孫` 形式で平坦化される。
  例: `totalPriceSet.shopMoney.amount` → `total_price_set__shop_money__amount`
- ネストした**配列**は子テーブル `親__フィールド` に分離され、`_dlt_parent_id` が親の `_dlt_id` を参照する。
  例: 注文の明細 → `orders__line_items` (`_dlt_parent_id` → `orders._dlt_id`)
- 監査列: 全テーブルに `_dlt_id` (行の一意 ID)、`_dlt_load_id` (ロードバッチ ID) が付与される。
