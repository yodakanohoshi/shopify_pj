# docs — テーブル定義書

Shopify 分析基盤の全レイヤのテーブル定義。1 テーブル = 1 ファイルで各ディレクトリに収録する。

```
Shopify Admin GraphQL API
   │  dataload/ (dlt: Bulk Operations + ページング)
   ▼
raw          ← raw_source_tables/
   │  elt/ (dbt)
   ▼
staging      ← staging_tables/
   ▼
intermediate ← intermediate_tables/
   ▼
marts        ← marts_tables/      ← BI / 分析はここを参照
```

| ディレクトリ | スキーマ | 生成 | テーブル数 |
|---|---|---|---|
| [`raw_source_tables/`](raw_source_tables/) | `raw` | dlt | 14 |
| [`staging_tables/`](staging_tables/) | `staging` | dbt (view) | 14 |
| [`intermediate_tables/`](intermediate_tables/) | `intermediate` | dbt (view) | 7 |
| [`marts_tables/`](marts_tables/) | `marts` | dbt (table) | 9 |

各ディレクトリの `README.md` に、そのレイヤのテーブル一覧と ER 概要を置く。

## 記法

- **型** は DuckDB / dbt 上の論理型。金額は Shopify API では文字列で返るため staging 以降で `double` に変換する。
- **PK** = 主キー、**FK** = 外部キー。
- ID は原則 Shopify の GraphQL global ID (`gid://shopify/<Type>/<n>`)。数値の legacy ID は `*_legacy_id`。
- 分析に有用なソースは dlt 標準非対応でもカスタム取得している (discounts / collections / abandoned_checkouts / locations)。

## dlt の正規化・Bulk の整形規則

- **Bulk 由来**の子テーブルは、各ノードの `__parentId` を `parent_id` に改名して親の gid を保持する
  (例: `order_line_items.parent_id` → `orders.id`)。
- ネストした**単一オブジェクト**は親テーブルに `親__子__孫` 形式で平坦化される
  (例: `totalPriceSet.shopMoney.amount` → `total_price_set__shop_money__amount`)。
- ネストした**inline list** (tags / discountCodes / selectedOptions 等) は dlt が子テーブル
  `親__フィールド` に分離し、`_dlt_parent_id` が親の `_dlt_id` を参照する。
- 監査列: 全テーブルに `_dlt_id` (行の一意 ID)、`_dlt_load_id` (ロードバッチ ID) が付与される。
