# 04. 分析基盤の仕組みと動かし方

トークンとデータが用意できたら、パイプラインを回して marts を作る。

## アーキテクチャ

```
Shopify Admin GraphQL API
   │  dataload/  (dlt)   … Bulk Operations + ページングで抽出
   ▼
 raw (DuckDB: shopify.duckdb / スキーマ raw)
   │  elt/  (dbt-duckdb)  … 変換
   ▼
 staging → intermediate → marts
   │
   ▼  分析 / BI が marts.* を参照
```

- **dlt** (data load tool): API → DuckDB へのロードを担う (`dataload/`)。
- **dbt**: SQL でモデルを段階的に変換する (`elt/`)。
- **DuckDB**: ファイル1つで完結する分析用 DB。dlt と dbt が同じファイルを共有する。

## 実行手順 (端から端まで)

```powershell
# 1. データ抽出 (source → raw)
cd dataload
uv sync
# 認証情報を設定 (.dlt/secrets.toml か .env)。shop は .dlt/config.toml
uv run python shopify_pipeline.py

# 2. 変換 (raw → marts)
cd ..\elt
uv sync
$env:PYTHONUTF8='1'          # 日本語コメントを含む Windows(cp932) 対策
uv run dbt build --profiles-dir .

# 3. 確認
uv run dbt docs generate --profiles-dir .
uv run dbt docs serve --profiles-dir .
```

## つまずきやすい点

| 症状 | 対処 |
|---|---|
| dbt が `cp932` で文字化けエラー | `PYTHONUTF8=1` を設定して再実行 |
| DuckDB が開けない/ロックされる | dlt ロードと dbt を**同時に**走らせない (単一ライタ) |
| Bulk が `already running` で失敗 | 直前の Bulk 完了待ち。パイプラインは自動でリソースを逐次実行する |
| データが 0 件 | ストアにデータが無い → [05. seed](05-seeding-data.md) で投入 |

## 出力の確認 (SQL)

```powershell
cd ..\dataload
uv run python -c "import duckdb; c=duckdb.connect('shopify.duckdb'); print(c.sql('select * from marts.fct_orders limit 5'))"
```

marts の各テーブルは [`../../docs/marts_tables/`](../../docs/marts_tables/) を参照。

次は [05. 初期データ投入 (seed)](05-seeding-data.md)。
