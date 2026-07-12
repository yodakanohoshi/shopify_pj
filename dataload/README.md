# dataload — Shopify → raw (dlt / DuckDB)

Shopify 開発ストアの Admin GraphQL API からデータを抽出し、DuckDB の `raw` スキーマへロードする [dlt](https://dlthub.com/) パイプライン。

分析に有用なソースは、dlt 標準ソースが非対応でも discounts と同様にカスタム取得する。

## 取得モード

運用は2モードを前提とする。

- **差分取得 (既定)** — 日次/毎時のスケジュール実行向け。前回実行で記録した高水位
  (`updated_at` / 放棄チェックアウトは `created_at`) 以降だけを Shopify 側の検索フィルタで
  絞って取得し、`merge` で upsert する。**Bulk も差分**で、connection に
  `(query: "updated_at:>=...")` を注入して更新分だけをエクスポートする。
  初回実行は高水位が無いため自動的に全件取得 (= 初回バックフィル) になる。
- **バックフィル (手動・随時)** — 過去分をまとめて取り直すとき。保存済み高水位を無視して
  全期間、または `--start` / `--end` の期間を再取得する。高水位は前進のみ
  (過去窓の再取得で巻き戻さない)。

大きく変動しない小さなディメンション (discounts / locations) は差分に載せず、毎回
`replace` で全件洗い替えする (件数が少なく安全側)。

## 取得方式

- **Bulk Operations** (`shopify_source/bulk.py`): 大きくネストするソースを1クエリでエクスポート。
  結果 JSONL の各ノードを gid の型で判定し、型ごとの raw テーブルへ振り分ける。
  子ノードは `__parentId` → `parent_id` として親の gid を保持する (join キー)。
  差分時はトップレベル connection に `(query: ...)` を注入し更新分のみをエクスポートする。
- **通常ページング** (`shopify_source/helpers.py`): 件数の少ない/Bulk に載せにくいソース向け。

Bulk 系リソースは `write_disposition="merge"` (primary_key=`id`) で upsert、
小さなディメンションは `replace` で全件洗い替え。

> merge は差分 upsert のため、親から取り除かれた子行 (削除された注文明細やコレクション
> 非所属化) は残る。厳密に整合させたいときは `--backfill` で全期間を取り直す。

## 取得対象リソース

| ソース | 方式 | 生成される raw テーブル |
|---|---|---|
| 注文 | Bulk | `orders`, `order_line_items`, `orders__refunds`, `orders__fulfillments`, `orders__transactions` (返金/出荷/取引は inline list 子) |
| 商品 | Bulk | `products`, `product_variants` (原価 `inventory_item__unit_cost` / 在庫 `inventory_item__id` 含む) |
| 顧客 | Bulk | `customers` (メール配信同意含む), `customer_addresses` |
| コレクション | Bulk | `collections`, `collection_products` (商品所属) |
| 放棄チェックアウト | Bulk | `abandoned_checkouts`, `abandoned_checkout_line_items` |
| 在庫レベル | Bulk (全件) | `inventory_levels`, `inventory_levels__quantities` (locations→inventoryLevels) |
| 割引 | ページング | `discounts`, `discounts__codes` (**dlt 標準非対応**・`discountNodes`) |
| ロケーション | ページング | `locations` |

> Bulk 制約: 1クエリ connection 最大5・ネスト最大2階層・ノードは Node(id)必須。
> このため注文の割引適用 (`discountApplications`, Node 非実装) は Bulk 対象外とし、
> 注文の `discount_codes` (コード文字列) と `discounts` ディメンションで代替する。
> 返金/出荷/取引 (`refunds`/`fulfillments`/`transactions`) はコネクションでなく
> リスト型のため、注文ノードに inline 展開され dlt が `orders__*` 子テーブルへ正規化する
> (connection 枠を消費しない)。
> 在庫レベルは差分キーが無いため毎回全件取得 (`replace`)。
> 同時に実行できる Bulk operation は1つのみ (リソースは逐次実行される)。

## セットアップ

```powershell
# 依存解決 (uv が Python も含めて用意する)
uv sync

# 認証情報を設定 (どちらか一方でよい)
Copy-Item .dlt\secrets.toml.example .dlt\secrets.toml   # client_id / client_secret を記入
#   または
Copy-Item .env.example .env                              # SHOPIFY_CLIENT_ID / SHOPIFY_CLIENT_SECRET を記入

# shop / api_version は .dlt/config.toml で設定
```

Dev Dashboard アプリの **Client ID / Secret** を設定すると、実行時に Client Credentials Grant で
アクセストークン (24h) を自動取得・更新する。固定トークン (App Automation Token 等) を使う場合は
`access_token` / `SHOPIFY_ACCESS_TOKEN` のみ設定する。取得手順は
[`../shopifystore/README.md`](../shopifystore/README.md) / [`../shopifystore/docs/02-dev-store-and-app.md`](../shopifystore/docs/02-dev-store-and-app.md) を参照。

## 実行

```powershell
# 差分取得 (既定・日次/毎時のスケジュール実行向け)
uv run python shopify_pipeline.py

# 全期間バックフィル (手動・随時)
uv run python shopify_pipeline.py --backfill

# 期間指定バックフィル (手動・随時)
uv run python shopify_pipeline.py --start 2025-01-01 --end 2025-03-31
```

- 出力先 DuckDB: `shopify.duckdb` (環境変数 `SHOPIFY_DUCKDB_PATH` で変更可)
- スキーマ: `raw`
- 既定は差分取得。前回の高水位以降のみを Bulk 側フィルタで絞って取得し `merge` する
  (初回は高水位が無いため全件取得 = 初回バックフィル)。
- 高水位は dlt のパイプライン状態に保存される。別ファイルに出力するときや状態を
  リセットしたいときは `--backfill` で取り直す。

## 出力の確認

```powershell
uv run python -c "import duckdb; con=duckdb.connect('shopify.duckdb'); print(con.sql('SHOW ALL TABLES'))"
```

生成される raw テーブルの定義は [`../docs/01-raw-source-tables.md`](../docs/01-raw-source-tables.md) を参照。

## 構成

```
dataload/
├─ shopify_pipeline.py        # エントリポイント (dlt.pipeline → DuckDB raw)
├─ shopify_source/
│  ├─ __init__.py             # @dlt.source と各 @dlt.resource (Bulk/ページング)
│  ├─ bulk.py                 # Bulk Operations 実行 + JSONL 型振り分け
│  ├─ helpers.py              # GraphQL クライアント / ページング / edges 畳み込み
│  └─ queries.py              # Bulk / ページング クエリ定義
└─ .dlt/
   ├─ config.toml             # shop / api_version 等の非機密設定
   └─ secrets.toml(.example)  # access_token (git 管理外)
```
