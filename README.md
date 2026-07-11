# Shopify 分析基盤

Shopify **開発ストア (development store)** を対象にした、dlt + dbt + DuckDB のローカル分析基盤。

```
Shopify Admin GraphQL API
   │
   ▼  dataload/   dlt         抽出・ロード (source → raw)
 raw (DuckDB)
   │
   ▼  elt/        dbt-duckdb  変換 (raw → staging → intermediate → marts)
 marts (dim / fct)
   │
   ▼  BI / 分析
```

## ディレクトリ

| ディレクトリ | 役割 | スタック |
|---|---|---|
| [`shopifystore/`](shopifystore/) | 開発ストアの構築手順 (初心者向け [docs/](shopifystore/docs/)) + 初期データ投入 | Shopify Partner / Admin API / Python |
| [`dataload/`](dataload/) | データロード (source → raw)。Bulk Operations + 割引等のカスタム取得 | dlt / DuckDB |
| [`elt/`](elt/) | データ変換 (raw → stg → intermediate → marts) | dbt-duckdb |
| [`docs/`](docs/) | 全レイヤのテーブル定義書 (レイヤ別ディレクトリ・1テーブル1ファイル) | Markdown |

## 取得している分析ソース

注文 / 商品 (原価) / 顧客 (配信同意) / コレクション / 放棄チェックアウト / 割引 / ロケーション。
分析に有用なソースは dlt 標準非対応でも割引と同じ要領でカスタム取得している。
大きくネストするソースは **Bulk Operations** で全件エクスポートし、型ごとの raw テーブルへ振り分ける。

DuckDB ファイル (`dataload/shopify.duckdb`) を dlt と dbt で共有する。

## クイックスタート

```powershell
# 0. 開発ストア構築 + 初期データ投入 (初回のみ)
#    shopifystore/README.md に従い Partner ストア作成 → Admin API トークン取得
cd shopifystore\seed; uv sync; uv run python seed.py

# 1. 抽出・ロード (source → raw)
cd ..\..\dataload; uv sync; uv run python shopify_pipeline.py

# 2. 変換 (raw → marts)
cd ..\elt; uv sync
$env:PYTHONUTF8='1'                     # 日本語コメントを含む Windows(cp932) 対策
uv run dbt build --profiles-dir .

# 3. 分析 — marts.fct_orders / fct_order_lines / fct_discount_performance / dim_* を参照
```

## 前提ツール

- [uv](https://docs.astral.sh/uv/) (Python 管理) — 導入済み
- Node.js LTS + [@shopify/cli](https://shopify.dev/docs/api/shopify-cli) — 導入済み (テーマ/アプリ開発は任意)
- Shopify Partner アカウント (無料) と開発ストア — [`shopifystore/README.md`](shopifystore/README.md) 参照

## メモ

- **割引 (discounts)** は dlt 標準ソースが未対応のため、GraphQL `discountNodes` を叩く
  カスタムリソースとして [`dataload/shopify_source/`](dataload/shopify_source/) に実装している。
- Windows の日本語ロケール (cp932) では dbt 実行時に `PYTHONUTF8=1` を設定する
  (プロジェクト内の日本語コメント読み込みのため)。
- DuckDB は単一ライタ。dlt ロードと dbt 実行を同時に走らせないこと。
