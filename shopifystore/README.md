# shopifystore — 開発ストアの構築と初期データ投入

無料の Shopify **開発ストア (development store)** を用意し、分析基盤 (dataload/elt) が取り込む
元データ (商品・顧客・コレクション・**割引**・注文) を Admin API 経由で投入するための手順とスクリプト。

> **Shopify が初めての方へ**: 用語・ストア作成・データモデル・システムの仕組みを順に解説した
> ガイドを [`docs/`](docs/) に用意した。まずそちらを読むのが近道。

## 全体像

```
Dev Dashboard (dev.shopify.com/dashboard)
   ├─ Stores → 開発ストア作成
   └─ Apps   → アプリ作成 → スコープ設定 → 開発ストアにインストール → Client ID / Secret
                  ├─ seed/     … Client Credentials Grant でトークン自動取得しデータ投入
                  └─ dataload/ … 同上でトークン自動取得し抽出
```

> **2026年1月以降、開発は Dev Dashboard に一本化**され、ストア内カスタムアプリ (`shpat_`) は廃止。
> Dev Dashboard アプリは固定トークンではなく **Client ID / Secret** を発行し、
> 実行時に **Client Credentials Grant** でアクセストークン (24h) に交換する
> （本プロジェクトのスクリプトが自動で取得・更新する）。
> 手順の詳細は初心者向けガイド [`docs/02-dev-store-and-app.md`](docs/02-dev-store-and-app.md) を参照。

---

## 1. 開発ストアの作成（Dev Dashboard）

1. <https://dev.shopify.com/dashboard> にログイン（Shopify / Partner アカウント）。
   - 別ルート: Shopify Admin の右上ストア名 → **Dev Dashboard**、または
     Partner Dashboard → **App distribution** → **Visit Dev Dashboard**。
2. **Stores** タブ → **Create store** → **Development store (Dev store)**。
3. ストア名 = `xxxx.myshopify.com` の `xxxx`（= `SHOPIFY_SHOP`）。無料・無期限・本番販売不可。

## 2. アプリ作成 → Client ID / Secret 取得（Dev Dashboard）

1. **Apps** タブ → **Create app** → **Start from Dev Dashboard** → 名前を付けて **Create**。
2. アプリの構成で **アクセススコープ**を設定（バージョンを作成して保存）:
   - 読み取り: `read_orders`, `read_products`, `read_customers`, `read_discounts`, `read_inventory`, `read_locations`
   - シード投入も行うなら `write_products`, `write_customers`, `write_discounts`, `write_draft_orders`, `write_orders`
3. **保護対象顧客データアクセスを有効化**（顧客・注文の顧客情報に必須。未承認だと `ACCESS_DENIED`）:
   アプリの **API access → Protected customer data access → Request access** → **Level 2**（氏名/メール/電話/住所）
   と全フィールドを選択 → データ保護詳細を入力。**開発ストアは審査不要で即時有効化**。
4. 左パネル **Home** → **Install app** → ステップ 1 の開発ストアにインストール。
5. アプリ → **Settings** で **Client ID** と **Client secret** をコピー。

この Client ID / Secret を:
- 抽出用に `dataload/.dlt/secrets.toml`（`client_id` / `client_secret`）または `dataload/.env`
- シード投入用に `shopifystore/seed/.env`（`SHOPIFY_CLIENT_ID` / `SHOPIFY_CLIENT_SECRET`）

へ設定する。スクリプトが Client Credentials Grant でアクセストークン (24h) を自動取得する。

> **代替**: CI/自動化向けに、アプリ → Settings → **App Automation Token** で 1/3/6か月有効の
> 固定トークンを発行し、`SHOPIFY_ADMIN_TOKEN`（seed）/ `access_token`（dataload）に設定してもよい。
> 古い無効な `SHOPIFY_ADMIN_TOKEN` が残っていると優先されて 401 になるので削除すること。

## 3. 初期データの投入 (seed)

`seed/` は Admin GraphQL API で商品・顧客・**割引**・注文 (ドラフト注文の確定) を作成する。
Shopify 標準のテストデータ生成では割引が十分に作られないため、割引を明示的に投入するのが目的。

```powershell
cd shopifystore\seed
uv sync
Copy-Item .env.example .env    # SHOPIFY_SHOP / SHOPIFY_CLIENT_ID / SHOPIFY_CLIENT_SECRET を記入

uv run python seed.py          # 全件投入
# 個別に投入する場合:
uv run python seed.py --only products,customers,discounts,orders
```

投入内容 (既定):
- 商品 8 件 (価格 + **原価**付き → 粗利分析)
- 顧客 5 件 (メール配信同意あり/なし → セグメント分析)
- コレクション 3 件 (商品所属付き → カテゴリ分析)
- 割引 4 件 (定率コード / 定額コード / 送料無料コード / 自動割引)
- 注文 10 件 (ドラフト注文を確定。一部に手動割引を適用)

詳細は [`docs/05-seeding-data.md`](docs/05-seeding-data.md)。

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
