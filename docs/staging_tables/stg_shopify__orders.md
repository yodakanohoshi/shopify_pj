# staging.stg_shopify__orders

注文ヘッダ (クレンジング済み)。元: `raw.orders`。粒度: 1 行 = 1 注文。

| カラム | 型 | 説明 |
|---|---|---|
| order_id | varchar | 注文 ID。**PK** |
| order_legacy_id | varchar | 数値 legacy 注文 ID |
| order_name | varchar | 注文名 (`#1001`) |
| customer_id | varchar | 顧客 ID (FK、ゲストは null) |
| financial_status / fulfillment_status | varchar | 支払 / 配送ステータス |
| source_name | varchar | 注文チャネル |
| currency_code | varchar | 通貨 |
| email / phone / note | varchar | 連絡先・備考 |
| ship_city / ship_province / ship_country / ship_country_code / ship_zip | varchar | 配送先 |
| total_price / subtotal_price / total_tax / total_discounts / total_shipping | double | 各金額 (作成時点) |
| current_total_price | double | 返金反映後の現在合計 |
| total_refunded | double | 返金総額 |
| created_at / updated_at / processed_at / cancelled_at / closed_at | timestamp | 各日時 |
| order_dlt_id | varchar | inline list 子 (discount_codes) 結合用 dlt 行 ID |
