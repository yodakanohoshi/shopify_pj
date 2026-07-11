# raw.orders

注文ヘッダ。取得方式: **Bulk** (`orders`)。粒度: 1 行 = 1 注文。

| カラム | 型 | 説明 |
|---|---|---|
| id | varchar | 注文 global ID (`gid://shopify/Order/...`)。**PK** |
| legacy_resource_id | varchar | 数値の legacy 注文 ID |
| name | varchar | 注文名 (例 `#1001`) |
| created_at / updated_at | varchar(ISO8601) | 作成 / 更新日時 |
| processed_at / cancelled_at / closed_at | varchar | 処理 / キャンセル / クローズ日時 |
| display_financial_status | varchar | 支払ステータス (PAID, PENDING, REFUNDED 等) |
| display_fulfillment_status | varchar | 配送ステータス (FULFILLED, UNFULFILLED 等) |
| currency_code | varchar | 通貨コード |
| source_name | varchar | 注文チャネル (web, pos, mobile_app 等) |
| email / phone / note | varchar | 連絡先・備考 |
| tags | (子: orders__tags) | タグ (inline list) |
| discount_codes | (子: orders__discount_codes) | 適用割引コード文字列 (inline list) |
| customer__id | varchar | 注文者顧客 ID (FK → customers.id、ゲストは null) |
| shipping_address__city / __province / __country / __country_code_v2 / __zip | varchar | 配送先住所 |
| billing_address__city / __province / __country / __country_code_v2 / __zip | varchar | 請求先住所 |
| total_price_set__shop_money__amount | varchar(数値) | 合計金額 (作成時点) |
| subtotal_price_set__shop_money__amount | varchar(数値) | 小計 |
| current_total_price_set__shop_money__amount | varchar(数値) | 返金反映後の現在合計 |
| total_tax_set__shop_money__amount | varchar(数値) | 税額 |
| total_discounts_set__shop_money__amount | varchar(数値) | 割引総額 |
| total_shipping_price_set__shop_money__amount | varchar(数値) | 送料 |
| total_refunded_set__shop_money__amount | varchar(数値) | 返金総額 |

子テーブル: [order_line_items](order_line_items.md) (parent_id → id)、[orders__discount_codes](orders__discount_codes.md) (_dlt_parent_id → _dlt_id)。
