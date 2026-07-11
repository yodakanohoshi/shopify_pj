# dataload — Shopify → raw (dlt / DuckDB)

Shopify 開発ストアの Admin GraphQL API からデータを抽出し、DuckDB の `raw` スキーマへロードする [dlt](https://dlthub.com/) パイプライン。

分析に有用なソースは、dlt 標準ソースが非対応でも discounts と同様にカスタム取得する。

## 取得方式

- **Bulk Operations** (`shopify_source/bulk.py`): 大きくネストするソースを1クエリで全件エクスポート。
  結果 JSONL の各ノードを gid の型で判定し、型ごとの raw テーブルへ振り分ける。
  子ノードは `__parentId` → `parent_id` として親の gid を保持する (join キー)。
- **通常ページング** (`shopify_source/helpers.py`): 件数の少ない/Bulk に載せにくいソース向け。

いずれも `write_disposition="replace"` の全件洗い替え (Bulk は全件エクスポートのため)。

## 取得対象リソース

| ソース | 方式 | 生成される raw テーブル |
|---|---|---|
| 注文 | Bulk | `orders`, `order_line_items` |
| 商品 | Bulk | `products`, `product_variants` (原価 `inventory_item__unit_cost` 含む) |
| 顧客 | Bulk | `customers` (メール配信同意含む), `customer_addresses` |
| コレクション | Bulk | `collections`, `collection_products` (商品所属) |
| 放棄チェックアウト | Bulk | `abandoned_checkouts`, `abandoned_checkout_line_items` |
| 割引 | ページング | `discounts`, `discounts__codes` (**dlt 標準非対応**・`discountNodes`) |
| ロケーション | ページング | `locations` |

> Bulk 制約: 1クエリ connection 最大5・ネスト最大2階層・ノードは Node(id)必須。
> このため注文の割引適用 (`discountApplications`, Node 非実装) は Bulk 対象外とし、
> 注文の `discount_codes` (コード文字列) と `discounts` ディメンションで代替する。
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
uv run python shopify_pipeline.py
```

- 出力先 DuckDB: `shopify.duckdb` (環境変数 `SHOPIFY_DUCKDB_PATH` で変更可)
- スキーマ: `raw`
- 2回目以降は `updatedAt` の前回値以降のみ取得する増分ロード

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
