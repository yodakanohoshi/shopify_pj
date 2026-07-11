# shopifystore — 開発ストアの構築と初期データ投入

無料の Shopify **開発ストア (development store)** を用意し、分析基盤 (dataload/elt) が取り込む
元データ (商品・顧客・**割引**・注文) を Admin API 経由で投入するための手順とスクリプト。

## 全体像

```
Shopify Partner (無料)
   └─ 開発ストア作成
        └─ カスタムアプリ作成 → Admin API トークン (shpat_...)
             ├─ seed/  (このディレクトリのスクリプト) でデータ投入
             └─ dataload/ の dlt がこのトークンで抽出
```

---

## 1. Partner アカウントと開発ストア

1. <https://www.shopify.com/partners> で無料の Partner アカウントを作成。
2. Partner Dashboard → **Stores** → **Add store** → **Create development store**。
   - 用途: *Test and build* を選択。
   - 開発ストアは無料・無期限。ただし本番販売は不可 (分析検証には十分)。
3. 必要なら **Add test data** で商品・注文のサンプルを自動生成できる (任意)。

> 開発ストアは Shopify CLI では作成できない。CLI はテーマ/アプリ開発用。ストア作成は Partner Dashboard で行う。

## 2. カスタムアプリと Admin API トークン

1. 作成した開発ストアの管理画面 → **Settings** → **Apps and sales channels** → **Develop apps**。
2. **Create an app** → 名前を付ける (例 `analytics-loader`)。
3. **Configuration** → **Admin API integration** → 以下のスコープを付与:
   - `read_orders`, `read_products`, `read_customers`, `read_discounts`
   - シード投入も行うなら `write_products`, `write_customers`, `write_discounts`, `write_draft_orders`, `write_orders`
4. **Install app** → **Admin API access token** (`shpat_...`) を控える。**一度しか表示されない**。
5. API バージョンは `2025-01` を想定 (変更時は各所の設定を合わせる)。

このトークンを:
- 抽出用に `dataload/.dlt/secrets.toml` (または `dataload/.env`)
- シード投入用に `shopifystore/seed/.env`

へ設定する。

## 3. 初期データの投入 (seed)

`seed/` は Admin GraphQL API で商品・顧客・**割引**・注文 (ドラフト注文の確定) を作成する。
Shopify 標準のテストデータ生成では割引が十分に作られないため、割引を明示的に投入するのが目的。

```powershell
cd shopifystore\seed
uv sync
Copy-Item .env.example .env    # SHOPIFY_SHOP / SHOPIFY_ADMIN_TOKEN を記入

uv run python seed.py          # 全件投入
# 個別に投入する場合:
uv run python seed.py --only products,customers,discounts,orders
```

投入内容 (既定):
- 商品 6 件 (バリアント価格付き)
- 顧客 4 件
- 割引 4 件 (定率コード / 定額コード / 送料無料コード / 自動割引)
- 注文 8 件 (ドラフト注文を確定。一部に手動割引を適用)

## 4. Shopify CLI (任意)

テーマやアプリの雛形が必要になったとき:

```powershell
shopify version
shopify theme init      # テーマ雛形
shopify app init        # アプリ雛形
shopify auth login      # Partner 認証
```

分析基盤の構築自体に CLI は必須ではない (Admin API トークンで完結する)。

---

## 次のステップ

1. ここでトークンを取得し seed 投入 → `dataload/` で `uv run python shopify_pipeline.py`
2. `elt/` で `uv run dbt build --profiles-dir .`
3. `docs/` のテーブル定義書に沿って marts を分析

構成の全体像は各ディレクトリの README を参照:
[`../dataload/README.md`](../dataload/README.md) / [`../elt/README.md`](../elt/README.md) / [`../docs/README.md`](../docs/README.md)
