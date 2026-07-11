# 02. 開発ストアとカスタムアプリの作成

分析基盤が接続する「ストア」と「Admin API トークン」を用意する。所要 10〜15 分。

## ステップ 1: Partner アカウント

1. <https://www.shopify.com/partners> で無料の Partner アカウントを作成。
2. メール認証を済ませて Partner Dashboard に入る。

## ステップ 2: 開発ストアの作成

1. Partner Dashboard → **Stores** → **Add store** → **Create development store**。
2. 用途は **Test and build** を選択。
3. ストア名 (= `xxxx.myshopify.com` の `xxxx`) を決める。これが後で使う `SHOPIFY_SHOP`。
4. 開発ストアは無料・無期限。本番販売はできないが分析検証には十分。

> 任意: ストア作成時や管理画面から **サンプルデータ (test data)** を自動生成できるが、
> 割引やコレクションは十分に作られないため、本プロジェクトの [seed](05-seeding-data.md) を推奨。

## ステップ 3: カスタムアプリで API トークンを発行

1. 開発ストアの管理画面 → **Settings** → **Apps and sales channels** → **Develop apps**。
   - 初回は **Allow custom app development** を有効化する。
2. **Create an app** → 名前を付ける (例 `analytics-loader`)。
3. **Configuration** → **Admin API integration** → **アクセススコープ**を付与:

   | 目的 | スコープ |
   |---|---|
   | 分析基盤の抽出 (読み取り) | `read_orders`, `read_products`, `read_customers`, `read_discounts`, `read_inventory`, `read_locations`, `read_marketing_events` |
   | seed 投入 (書き込み) | `write_products`, `write_customers`, `write_discounts`, `write_draft_orders`, `write_orders` |

   > 放棄チェックアウトは `read_orders` の範囲で取得できる。迷ったら上記を全付与でよい (開発ストアのため)。

4. **Install app** → 表示される **Admin API access token** (`shpat_...`) を控える。
   **このトークンは一度しか表示されない**ので必ず保存する。
5. API バージョンは `2025-01` を想定 (アプリ設定の API version と合わせる)。

## ステップ 4: トークンを配置

| 用途 | 置き場所 | キー |
|---|---|---|
| データ抽出 | `dataload/.dlt/secrets.toml` または `dataload/.env` | `access_token` / `SHOPIFY_ACCESS_TOKEN` |
| seed 投入 | `shopifystore/seed/.env` | `SHOPIFY_ADMIN_TOKEN` |

`shop` (サブドメイン) は `dataload/.dlt/config.toml` と `shopifystore/seed/.env` に設定する。

次は [03. Shopify のデータモデル](03-data-model.md)。
