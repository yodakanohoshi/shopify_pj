# raw.orders

注文ヘッダ。取得方式: **Bulk** (`orders`)。粒度: 1 行 = 1 注文。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 注文ID | id | varchar | 注文 global ID (`gid://shopify/Order/...`)。**PK** |
| 注文レガシーID | legacy_resource_id | varchar | 数値の legacy 注文 ID |
| 注文名 | name | varchar | 注文名 (例 `#1001`) |
| 作成日時 / 更新日時 | created_at / updated_at | varchar(ISO8601) | 作成 / 更新日時 |
| 処理日時 / キャンセル日時 / クローズ日時 | processed_at / cancelled_at / closed_at | varchar | 処理 / キャンセル / クローズ日時 |
| 支払ステータス | display_financial_status | varchar | 支払ステータス (PAID, PENDING, REFUNDED 等) |
| 配送ステータス | display_fulfillment_status | varchar | 配送ステータス (FULFILLED, UNFULFILLED 等) |
| 通貨コード | currency_code | varchar | 通貨コード |
| 注文チャネル | source_name | varchar | 注文チャネル (web, pos, mobile_app 等) |
| メールアドレス / 電話番号 / 備考 | email / phone / note | varchar | 連絡先・備考 |
| タグ | tags | (子: orders__tags) | タグ (inline list) |
| 割引コード | discount_codes | (子: orders__discount_codes) | 適用割引コード文字列 (inline list) |
| 顧客ID | customer__id | varchar | 注文者顧客 ID (FK → customers.id、ゲストは null) |
| 配送先市区町村 / 配送先都道府県 / 配送先国 / 配送先国コード / 配送先郵便番号 | shipping_address__city / __province / __country / __country_code_v2 / __zip | varchar | 配送先住所 |
| 請求先市区町村 / 請求先都道府県 / 請求先国 / 請求先国コード / 請求先郵便番号 | billing_address__city / __province / __country / __country_code_v2 / __zip | varchar | 請求先住所 |
| 合計金額 | total_price_set__shop_money__amount | varchar(数値) | 合計金額 (作成時点) |
| 小計 | subtotal_price_set__shop_money__amount | varchar(数値) | 小計 |
| 現在合計金額 | current_total_price_set__shop_money__amount | varchar(数値) | 返金反映後の現在合計 |
| 税額 | total_tax_set__shop_money__amount | varchar(数値) | 税額 |
| 割引総額 | total_discounts_set__shop_money__amount | varchar(数値) | 割引総額 |
| 送料 | total_shipping_price_set__shop_money__amount | varchar(数値) | 送料 |
| 返金総額 | total_refunded_set__shop_money__amount | varchar(数値) | 返金総額 |

子テーブル: [order_line_items](order_line_items.md) (parent_id → id)、[orders__discount_codes](orders__discount_codes.md) (_dlt_parent_id → _dlt_id)。
