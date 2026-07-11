# 02. 開発ストアとアプリの作成（Dev Dashboard 方式）

分析基盤が接続する「ストア」と「Admin API トークン」を、Shopify の新しい
**Dev Dashboard** で用意する。所要 10〜15 分。

> Dev Dashboard は Shopify 開発の統合ハブ（アプリ・ストア・カタログを一元管理）。
> 公式: <https://shopify.dev/docs/apps/build/dev-dashboard>

## ステップ 1: Dev Dashboard にアクセス

- 直接: <https://dev.shopify.com/dashboard>（Shopify / Partner アカウントでログイン）
- 別ルート:
  - Shopify Admin から: 右上のストア名 → **Dev Dashboard**
  - 既存の Partner Dashboard から: **App distribution** → **Visit Dev Dashboard**

## ステップ 2: 開発ストアの作成

1. Dev Dashboard の **Stores** タブを開く。
2. **Create store**（または Add store）→ **Development store（Dev store）** を選択。
   - ストアの種類: *Dev stores*（アプリの構築・検証用。無料・本番販売不可）。
3. ストア名を決める。これが `xxxx.myshopify.com` の `xxxx` = 後で使う `SHOPIFY_SHOP`。
4. 作成後、**Stores** 一覧からストア Admin（管理画面）を開ける。

> 任意: ストア作成時にサンプルデータを入れられるが、割引・コレクションは十分に
> 作られないため、本プロジェクトの [seed](05-seeding-data.md) を推奨。

## ステップ 3: アプリ作成と Admin API トークン

Dev Dashboard には2つの作成方法がある。分析基盤はデータ取得（API 連携）が目的なので
**Dev Dashboard で直接作成する方法**（コード雛形なし）を使う。

1. **Apps** タブ → **Create app**。
2. **Create in Dev Dashboard**（＝バックエンド連携/自動化向け。アプリコードを生成せず、
   認証情報・権限・接続だけを素早く設定する方法）を選ぶ。
3. アプリの **Configuration / API access** で **Admin API のアクセススコープ**を付与:

   | 目的 | スコープ |
   |---|---|
   | 分析基盤の抽出（読み取り） | `read_orders`, `read_products`, `read_customers`, `read_discounts`, `read_inventory`, `read_locations` |
   | seed 投入（書き込み） | `write_products`, `write_customers`, `write_discounts`, `write_draft_orders`, `write_orders` |

   > 迷ったら開発ストアなので上記を全付与でよい。放棄チェックアウトは `read_orders` の範囲。

4. **ステップ 2 で作った開発ストアにインストール**（Install / Select store）。
5. インストール後、アプリの **Client credentials / API access** に表示される
   **Admin API access token** を控える（`X-Shopify-Access-Token` として使う値）。
   併せて **API key / API secret** も確認できる。**トークンは安全に保管**する。
6. API バージョンは `2025-01` を想定（アプリ設定の API version と合わせる）。

> **補足（従来方式）**: 単一ストアだけなら、ストア Admin → **Settings → Apps and sales
> channels → Develop apps** から作る「カスタムアプリ」で静的な `shpat_...` トークンを
> 得る方法も引き続き使える。どちらのトークンも本プロジェクトの取得処理でそのまま利用できる。

## ステップ 4: トークンを配置

| 用途 | 置き場所 | キー |
|---|---|---|
| データ抽出 | `dataload/.dlt/secrets.toml` または `dataload/.env` | `access_token` / `SHOPIFY_ACCESS_TOKEN` |
| seed 投入 | `shopifystore/seed/.env` | `SHOPIFY_ADMIN_TOKEN` |

`shop`（サブドメイン）は `dataload/.dlt/config.toml` と `shopifystore/seed/.env` に設定する。

次は [03. Shopify のデータモデル](03-data-model.md)。
