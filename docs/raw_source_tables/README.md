# raw ソーステーブル (`raw` スキーマ)

dlt が Shopify Admin GraphQL API から投入する生データ。列名 snake_case、ネストは `__` 平坦化。
全テーブルに監査列 `_dlt_id` / `_dlt_load_id` が付く (各ファイルでは省略)。

| テーブル | 取得方式 | 親 | 定義 |
|---|---|---|---|
| orders | Bulk | — | [orders.md](orders.md) |
| order_line_items | Bulk | orders | [order_line_items.md](order_line_items.md) |
| orders__discount_codes | Bulk (inline list) | orders | [orders__discount_codes.md](orders__discount_codes.md) |
| products | Bulk | — | [products.md](products.md) |
| product_variants | Bulk | products | [product_variants.md](product_variants.md) |
| customers | Bulk | — | [customers.md](customers.md) |
| customer_addresses | Bulk | customers | [customer_addresses.md](customer_addresses.md) |
| collections | Bulk | — | [collections.md](collections.md) |
| collection_products | Bulk | collections | [collection_products.md](collection_products.md) |
| abandoned_checkouts | Bulk | — | [abandoned_checkouts.md](abandoned_checkouts.md) |
| abandoned_checkout_line_items | Bulk | abandoned_checkouts | [abandoned_checkout_line_items.md](abandoned_checkout_line_items.md) |
| discounts | ページング | — | [discounts.md](discounts.md) |
| discounts__codes | ページング (子) | discounts | [discounts__codes.md](discounts__codes.md) |
| locations | ページング | — | [locations.md](locations.md) |

## 取得モードと書き込み方式

運用は2モードを前提とする (詳細は [`../../dataload/README.md`](../../dataload/README.md))。

- **差分取得 (既定)**: 日次/毎時のスケジュール実行。前回の高水位 (`updated_at`、
  放棄チェックアウトは `created_at`) 以降だけを Shopify 側フィルタで絞って取得する。
  **Bulk も差分**で、connection に `(query: "updated_at:>=...")` を注入する。
  初回は高水位が無いため全件取得 (= 初回バックフィル) になる。
- **バックフィル (手動・随時)**: 過去分をまとめて取り直すとき。保存済み高水位を無視して
  全期間または期間指定で再取得する。

書き込み方式はテーブルごとに次のとおり。

| 取得方式 | 対象 | 書き込み | 主キー |
|---|---|---|---|
| Bulk | orders / products / customers / collections / abandoned_checkouts と各子テーブル | `merge` (差分 upsert) | `id` |
| ページング | discounts / locations | `replace` (毎回全件洗い替え) | `id` |

> discounts / locations は件数が少なく変動も小さいため差分に載せず、毎回 `replace` する。
> `merge` は差分 upsert のため、親から取り除かれた子行 (削除された注文明細、コレクション
> 非所属化など) は残る。厳密に整合させたいときは全期間バックフィルで取り直す。

## 結合キーの規則

- **Bulk の子テーブル**: `parent_id` (親の gid) = 親テーブルの `id`。
- **inline list の子テーブル** (`*__discount_codes` 等): `_dlt_parent_id` = 親テーブルの `_dlt_id`。
