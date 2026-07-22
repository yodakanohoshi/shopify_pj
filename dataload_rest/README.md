# dataload_rest — REST API → raw (dlt / DuckDB)

ページングのある一般的な **REST API** からデータを抽出し、DuckDB の `raw` スキーマへロードする
[dlt](https://dlthub.com/) パイプライン。

[`../dataload/`](../dataload/) (Shopify Admin GraphQL 版) と**同じ構成・同じ運用**で、
取得方式だけを GraphQL/Bulk から REST + ページングに置き換えたもの。
認証フロー (Client Credentials Grant / 静的トークン) と取得モード (差分 / バックフィル) は同一。

## 取得モード

- **差分取得 (既定)** — 日次/毎時のスケジュール実行向け。前回実行で記録した高水位
  (`updated_at` 等) 以降だけを API 側のクエリパラメータ (`updated_since` 等) で絞って取得し、
  `merge` で upsert する。初回実行は高水位が無いため自動的に全件取得 (= 初回バックフィル) になる。
- **バックフィル (手動・随時)** — 過去分をまとめて取り直すとき。保存済み高水位を無視して
  全期間、または `--start` / `--end` の期間を再取得する。高水位は前進のみ
  (過去窓の再取得で巻き戻さない)。

大きく変動しない小さなディメンション (`incremental=False` のエンドポイント) は差分に載せず、
毎回 `replace` で全件洗い替えする。

## ページング方式

REST API はページングの流儀が API ごとに異なるため、代表的な4方式を実装している
(`rest_source/helpers.py` の `paginate`)。エンドポイントごとに `style` で選ぶ。

| `style` | 送るパラメータ | 終了条件 |
|---|---|---|
| `page` | `?page=1&per_page=100` | 取得件数が `page_size` 未満のページ |
| `offset` | `?offset=0&limit=100` | 取得件数が `page_size` 未満のページ |
| `cursor` | `?cursor=<前回応答の値>` | 応答に次カーソルが無い |
| `link` | 初回のみ。2ページ目以降は `Link` ヘッダの URL を追従 | `rel="next"` が無い |

レート制限は `Retry-After` / `X-RateLimit-Remaining` / `X-RateLimit-Reset` を尊重し、
429・5xx は指数バックオフで最大6回まで再試行する。

## 取得対象の設定

取得対象は [`rest_source/endpoints.py`](rest_source/endpoints.py) の `ENDPOINTS` に宣言的に並べる。
**対象 API に合わせて書き換えるのは基本的にこのファイルだけ**。

```python
Endpoint(
    name="orders",              # dlt リソース名 = 出力テーブル名
    path="orders",              # base_url からの相対パス
    data_path="data",           # 応答中のレコード配列の位置 (None ならトップレベルが配列)
    primary_key="id",
    style="page",               # ページング方式
    size_param="per_page",      # 件数パラメータ名
    cursor_field="updated_at",  # レコード側の更新時刻 (高水位の元)
    filter_param="updated_since",  # 高水位を渡すクエリパラメータ
    end_param="updated_until",     # 期間バックフィルの上限 (無ければ None)
)
```

差分に載せないディメンションは `incremental=False` を指定する (毎回全件・`replace`)。

> 同梱の定義は「`{"data": [...]}` を返し `updated_since` で絞れるページ番号ページング」という
> 一般的な形を仮定したサンプル。実 API のレスポンス形状に合わせて調整すること。

ネストしたオブジェクト/配列は dlt が自動で子テーブル (`<table>__<field>`) に正規化する。

## セットアップ

```powershell
# 依存解決 (uv が Python も含めて用意する)
uv sync

# 認証情報を設定 (どちらか一方でよい)
Copy-Item .dlt\secrets.toml.example .dlt\secrets.toml   # client_id / client_secret を記入
#   または
Copy-Item .env.example .env                              # REST_CLIENT_ID / REST_CLIENT_SECRET を記入

# base_url / token_url / page_size は .dlt/config.toml で設定
```

**Client ID / Secret** を設定すると、実行時に Client Credentials Grant でアクセストークンを
自動取得・更新する (`expires_in` を尊重し、失効60秒前に再取得)。
発行済みの固定トークンを使う場合は `access_token` / `REST_ACCESS_TOKEN` のみ設定する。

`Authorization: Bearer <token>` 以外のヘッダ形式が必要な API では、ソース引数
`auth_scheme` (例 `"Token"`、空文字でスキーム無し) や `RestClient(auth_header=...)` で調整する。

## 実行

```powershell
# 差分取得 (既定・日次/毎時のスケジュール実行向け)
uv run python rest_pipeline.py

# 全期間バックフィル (手動・随時)
uv run python rest_pipeline.py --backfill

# 期間指定バックフィル (手動・随時)
uv run python rest_pipeline.py --start 2025-01-01 --end 2025-03-31
```

- 出力先 DuckDB: `rest_api.duckdb` (環境変数 `REST_DUCKDB_PATH` で変更可)
- スキーマ: `raw`
- 高水位は dlt のパイプライン状態に保存される。リセットしたいときは `--backfill` で取り直す。

## 出力の確認

```powershell
uv run python -c "import duckdb; con=duckdb.connect('rest_api.duckdb'); print(con.sql('SHOW ALL TABLES'))"
```

## 構成

```
dataload_rest/
├─ rest_pipeline.py           # エントリポイント (dlt.pipeline → DuckDB raw)
├─ rest_source/
│  ├─ __init__.py             # @dlt.source と ENDPOINTS からの @dlt.resource 生成
│  ├─ endpoints.py            # 取得対象エンドポイントの宣言的定義 (ここを書き換える)
│  └─ helpers.py              # REST クライアント (認証/リトライ) / ページング
└─ .dlt/
   ├─ config.toml             # base_url / token_url 等の非機密設定
   └─ secrets.toml(.example)  # client_id / client_secret (git 管理外)
```

`dataload/` との対応:

| `dataload/` (Shopify GraphQL) | `dataload_rest/` (REST) |
|---|---|
| `shopify_pipeline.py` | `rest_pipeline.py` |
| `shopify_source/helpers.py` (GraphQL クライアント + カーソルページング) | `rest_source/helpers.py` (REST クライアント + 4方式ページング) |
| `shopify_source/queries.py` (GraphQL クエリ定義) | `rest_source/endpoints.py` (エンドポイント定義) |
| `shopify_source/bulk.py` (Bulk Operations) | 対応なし (REST は逐次ページング) |
