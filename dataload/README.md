# dataload — Shopify → raw (dlt / DuckDB)

Shopify 開発ストアの Admin GraphQL API からデータを抽出し、DuckDB の `raw` スキーマへロードする [dlt](https://dlthub.com/) パイプライン。

## 取得対象リソース

| リソース (raw テーブル) | API | 増分 | 備考 |
|---|---|---|---|
| `orders` | `orders` (GraphQL) | `updatedAt` merge | 明細 `orders__line_items`、割引適用 `orders__discount_applications` を子テーブルとして展開 |
| `customers` | `customers` (GraphQL) | `updatedAt` merge | |
| `products` | `products` (GraphQL) | `updatedAt` merge | バリアント `products__variants` を子テーブルへ展開 |
| `discounts` | `discountNodes` (GraphQL) | 全件 merge (id) | **dlt 標準ソース非対応**。コード割引・自動割引を統合取得。コードは `discounts__codes` |

> dlt はネストした配列を自動的に子テーブル (`<親>__<フィールド>`) へ正規化する。GraphQL の `edges/node` 構造は [`helpers.unwrap_connections`](shopify_source/helpers.py) で畳んでから渡している。

## セットアップ

```powershell
# 依存解決 (uv が Python も含めて用意する)
uv sync

# 認証情報を設定 (どちらか一方でよい)
Copy-Item .dlt\secrets.toml.example .dlt\secrets.toml   # access_token を記入
#   または
Copy-Item .env.example .env                              # SHOPIFY_* を記入

# shop / api_version は .dlt/config.toml で設定
```

Admin API トークンの取得手順は [`../shopifystore/README.md`](../shopifystore/README.md) を参照。

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
│  ├─ __init__.py             # @dlt.source と各 @dlt.resource
│  ├─ helpers.py              # GraphQL クライアント / ページング / edges 畳み込み
│  └─ queries.py              # GraphQL クエリ定義
└─ .dlt/
   ├─ config.toml             # shop / api_version 等の非機密設定
   └─ secrets.toml(.example)  # access_token (git 管理外)
```
