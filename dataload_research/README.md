# dataload_research — Shopify API 調査サンドボックス

**どんなデータが取れるか**を確かめるための実験ディレクトリ。本番の取り込み
([`../dataload/`](../dataload/)) とは独立しており、**dbt では扱わない**。Bulk を使わず
非 Bulk の GraphQL で数件だけ取得し、生 JSON / dlt 正規化スキーマを覗く。

新しいフィールドやリソースを本番へ入れる前に「実際に何が返るか」を素早く確認する用途。

## 構成

| ファイル | 役割 |
|---|---|
| `queries.py` | 調査用の非 Bulk クエリ集 (`PROBES`)。本番に無い metafields / media / options 等も含む |
| `shopify_client.py` | 自己完結の最小 GraphQL クライアント (Client Credentials / 静的トークン) |
| `raw_probe.py` | **requests** で直接叩き、生 JSON を `samples/<name>.json` に保存 + 概要表示 |
| `dlt_probe.py` | **dlt** で `research.duckdb` にロードし、dlt が生成する正規化スキーマを表示 |

生成物 (`samples/`, `research.duckdb`, `.env`) は `.gitignore` 済み。

## セットアップ

```bash
cd dataload_research
uv sync                       # or: uv venv && uv pip install -e .
cp .env.example .env          # SHOPIFY_SHOP と認証情報を記入
```

認証は本番 `dataload/` と同じ開発ストア/アプリを流用してよい。

## 使い方

### 1. 生 JSON を覗く (requests)

```bash
uv run python raw_probe.py --list                 # プローブ一覧
uv run python raw_probe.py                         # 全部 3 件ずつ
uv run python raw_probe.py --only products -n 5    # products だけ 5 件
```

`samples/products.json` などに整形済み JSON が出力される。ネストした `edges/node` は
読みやすいよう素直なリストへ畳んである。

### 2. dlt の正規化を覗く (dlt → DuckDB)

```bash
uv run python dlt_probe.py --only products customers -n 5
```

`research.duckdb` (dataset `research`) にロードし、生成テーブルと列を一覧表示する。
`tags` のような scalar リストが子テーブル (`products__tags` 等) に割れる様子や、
ネストが `親__子` に平坦化される様子を、本番 DB を汚さず確認できる。

## 注意

- あくまで調査用。差分取得・merge・高水位管理などは持たない (毎回 `replace` / 単発取得)。
- `samples/` には実データが入るためコミットしない。
- 本番へ取り込みたいフィールドが定まったら [`../dataload/shopify_source/queries.py`](../dataload/shopify_source/queries.py) 側へ反映する。
