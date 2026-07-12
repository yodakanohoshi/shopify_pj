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
大きくネストするソースは **Bulk Operations** でエクスポートし、型ごとの raw テーブルへ振り分ける。

取得は**差分が既定** (日次/毎時のスケジュール実行を想定)。前回の高水位以降だけを
Bulk 側フィルタで絞って取得し `merge` する。過去分は**手動でバックフィル**する
(`dataload/README.md` 参照)。

DuckDB ファイル (`dataload/shopify.duckdb`) を dlt と dbt で共有する。

## 実行手順 (最初 → marts 生成)

リポジトリルート起点。**DuckDB は単一ライタ**のため dlt ロードと dbt 実行を同時に走らせないこと。
初回は **必ず バックフィル(手順2)→ dbt(手順3)の順**。新カラムが raw に入る前に dbt を走らせると列不足で落ちる。

```powershell
# 0. 認証設定 (初回のみ・設定済みなら省略)
#    shopifystore/README.md に従い開発ストア + Admin API 認証を用意し、
#    dataload/.dlt/secrets.toml (Client ID/Secret か access_token) と
#    dataload/.dlt/config.toml (shop) を設定する。
#    (任意) 初期サンプルデータ投入:
cd shopifystore\seed; uv sync; uv run python seed.py; cd ..\..

# 1. dataload: 依存解決
cd dataload; uv sync

# 2. 初回バックフィル (全件ロード。新カラム・新テーブルを含む)
uv run python shopify_pipeline.py --backfill
#    ロード確認:
uv run python -c "import duckdb; c=duckdb.connect('shopify.duckdb'); print(c.sql('SHOW ALL TABLES'))"

# 3. elt(dbt): 変換 (raw → staging → intermediate → marts)
cd ..\elt; uv sync
$env:PYTHONUTF8 = "1"                    # 日本語コメントを含む Windows(cp932) 対策・ターミナルごとに1回
uv run dbt parse --profiles-dir .        # refs/yml 検証 (DB 接続不要)
uv run dbt build --profiles-dir .        # モデル生成 + テスト (marts まで)

# 4. marts 確認
uv run python -c "import duckdb; c=duckdb.connect('../dataload/shopify.duckdb'); print(c.sql('SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema IN (''staging'',''intermediate'',''marts'') ORDER BY 1,2'))"
```

分析は `marts.fct_orders` / `fct_order_lines` / `fct_refunds` / `fct_fulfillments` /
`fct_order_transactions` / `fct_inventory_levels` / `fct_discount_performance` / `fct_abandoned_checkouts` /
`dim_customers` / `dim_products` / `dim_collections` / `dim_locations` を参照する。

### 定常運用 (差分)

```powershell
# 1) 差分取得 (日次/毎時)
cd dataload; uv run python shopify_pipeline.py
# 2) 変換
cd ..\elt; $env:PYTHONUTF8 = "1"; uv run dbt build --profiles-dir .
```

過去分を取り直すときは `uv run python shopify_pipeline.py --backfill`
(期間指定は `--start 2025-01-01 --end 2025-03-31`)。詳細は [`dataload/README.md`](dataload/README.md)。

## 前提ツール

- [uv](https://docs.astral.sh/uv/) (Python 管理) — 導入済み
- Node.js LTS + [@shopify/cli](https://shopify.dev/docs/api/shopify-cli) — 導入済み (テーマ/アプリ開発は任意)
- Shopify 開発ストア + Admin API トークン — [Dev Dashboard](https://dev.shopify.com/dashboard) で用意 ([`shopifystore/README.md`](shopifystore/README.md) 参照)

## メモ

- **割引 (discounts)** は dlt 標準ソースが未対応のため、GraphQL `discountNodes` を叩く
  カスタムリソースとして [`dataload/shopify_source/`](dataload/shopify_source/) に実装している。
- Windows の日本語ロケール (cp932) では dbt 実行時に `PYTHONUTF8=1` を設定する
  (プロジェクト内の日本語コメント読み込みのため)。
- DuckDB は単一ライタ。dlt ロードと dbt 実行を同時に走らせないこと。
