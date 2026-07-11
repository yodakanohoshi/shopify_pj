# 02. 開発ストアとアプリの作成（Dev Dashboard 方式）

分析基盤が接続する「ストア」と「Admin API 認証情報」を、Shopify の **Dev Dashboard** で用意する。

> **2026年1月以降、Shopify の開発は Dev Dashboard に一本化**され、ストア管理画面の
> 「Develop apps（カスタムアプリ / `shpat_` トークン）」は廃止された。
> 公式: <https://shopify.dev/docs/apps/build/dev-dashboard>

## 認証の仕組み（重要）

Dev Dashboard のアプリでは、UI に固定トークンは表示されない。代わりに
**Client ID / Client Secret** が発行され、これを **Client Credentials Grant** で
**アクセストークン（24時間で失効）** に交換して API を呼ぶ。

本プロジェクトのスクリプトは **Client ID / Secret を渡せば、トークン取得・更新を自動で行う**。
つまり利用者が用意するのは `SHOPIFY_CLIENT_ID` と `SHOPIFY_CLIENT_SECRET` の2つ。

## ステップ 1: Dev Dashboard にアクセス

- 直接: <https://dev.shopify.com/dashboard>（Shopify / Partner アカウントでログイン）
- 別ルート: Shopify Admin 右上のストア名 → **Dev Dashboard**、または
  Partner Dashboard → **App distribution** → **Visit Dev Dashboard**

## ステップ 2: 開発ストアの作成

1. **Stores** タブ → **Create store** → **Development store（Dev store）**。
2. ストア名 = `xxxx.myshopify.com` の `xxxx`（= `SHOPIFY_SHOP`）。無料・無期限・本番販売不可。

## ステップ 3: アプリの作成とスコープ設定

1. **Apps** タブ → 右上 **Create app** → **Start from Dev Dashboard**（コードを生成しない構成）→
   名前を付けて **Create**。
2. アプリの構成で **アクセススコープ（access scopes）** を設定:

   | 目的 | スコープ |
   |---|---|
   | 分析基盤の抽出（読み取り） | `read_orders`, `read_products`, `read_customers`, `read_discounts`, `read_inventory`, `read_locations` |
   | seed 投入（書き込み） | `write_products`, `write_customers`, `write_discounts`, `write_draft_orders`, `write_orders` |

   > 開発ストアなので迷ったら上記を全付与でよい。放棄チェックアウトは `read_orders` の範囲。
   > 設定はアプリの「バージョン」を作成して保存する形になる（Webhooks API version は最新でよい）。

## ステップ 4: 開発ストアへインストール

1. アプリ画面の左パネル **Home** → 下にスクロールして **Install app**。
2. ステップ 2 で作った開発ストアを選択（または作成）して **Install**。

> インストールしていないと、後述のトークン取得が 401 になる。

## ステップ 5: Client ID / Secret を取得して配置

1. アプリ画面 → **Settings** → **Client ID** と **Client secret** をコピー。
2. 置き場所:

   | 用途 | 置き場所 | キー |
   |---|---|---|
   | データ抽出 | `dataload/.dlt/secrets.toml` または `dataload/.env` | `client_id` / `client_secret`（env は `SHOPIFY_CLIENT_ID` / `SHOPIFY_CLIENT_SECRET`） |
   | seed 投入 | `shopifystore/seed/.env` | `SHOPIFY_CLIENT_ID` / `SHOPIFY_CLIENT_SECRET` |

3. `shop`（サブドメイン）は `dataload/.dlt/config.toml` と `shopifystore/seed/.env` に設定。
4. API バージョンは `2025-01` を想定（アプリ設定と合わせる）。

> **既に古い `SHOPIFY_ADMIN_TOKEN` を .env に書いている場合は削除/コメントアウトする。**
> 固定トークンが設定されているとそちらが優先され、無効な値だと 401 になる。

## （代替）App Automation Token を使う場合

CI/自動化向けに、**1/3/6か月**有効の固定トークンを発行することもできる。
アプリ → **Settings** → **App Automation Token** → **Create token**（作成直後のみ表示）。
この場合は Client ID/Secret の代わりに、そのトークンを
`SHOPIFY_ADMIN_TOKEN`（seed）/ `access_token`（dataload）に設定する。

次は [03. Shopify のデータモデル](03-data-model.md)。
