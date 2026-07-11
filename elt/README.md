# elt — dbt 変換 (raw → stg → intermediate → marts)

dlt が投入した DuckDB `raw` スキーマを、[dbt-duckdb](https://github.com/duckdb/dbt-duckdb) で分析用モデルへ変換する。

## レイヤ構成

```
raw (source: shopify_raw)         ← dataload/ の dlt が投入
  │
  ▼ staging  (schema: staging, view)      1:1 クレンジング・型付け・リネーム
  │    stg_shopify__orders / order_lines / order_discount_applications
  │    stg_shopify__customers / products / product_variants
  │    stg_shopify__discounts / discount_codes
  ▼ intermediate (schema: intermediate, view)  結合・集計の中間表現
  │    int_orders__enriched / int_order_lines__enriched / int_discounts__enriched
  ▼ marts    (schema: marts, table)        分析・BI が参照する最終形
       core/      dim_customers / dim_products / fct_orders / fct_order_lines
       marketing/ fct_discount_performance
```

命名は dbt 推奨規約 (`stg_<source>__<entity>`, `dim_`, `fct_`, `int_`) に従う。

## セットアップ

```powershell
cd elt
uv sync           # dbt-duckdb を用意
```

> 外部 dbt パッケージ (dbt_utils 等) には依存しない。テストは dbt 組込みの
> `unique` / `not_null` / `accepted_values` / `relationships` のみで構成している。

DuckDB ファイルは `dataload/` の dlt 出力と同一物理ファイル (`../dataload/shopify.duckdb`)。
`SHOPIFY_DUCKDB_PATH` で上書き可能。プロファイルは同梱の `profiles.yml` を使う。

## 実行

```powershell
# 依存関係の解析のみ (DB 接続不要)
uv run dbt parse --profiles-dir .

# 変換の実行 (要: dataload の dlt が raw を投入済み)
uv run dbt build --profiles-dir .

# ドキュメント生成 & 閲覧
uv run dbt docs generate --profiles-dir .
uv run dbt docs serve   --profiles-dir .
```

> DuckDB は単一ライタ。dlt ロードと dbt 実行を**同時に**走らせないこと。

## モデルの利用例

```sql
-- marts を直接参照
select order_date, sum(net_revenue) as revenue
from marts.fct_orders
group by 1 order by 1;
```

各層のカラム定義は [`../docs/`](../docs/) のテーブル定義書を参照。
