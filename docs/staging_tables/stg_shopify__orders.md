# staging.stg_shopify__orders

注文ヘッダ (クレンジング済み)。元: `raw.orders`。粒度: 1 行 = 1 注文。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 注文ID | order_id | varchar | 注文 ID。**PK** |
| 注文レガシーID | order_legacy_id | varchar | 数値 legacy 注文 ID |
| 注文名 | order_name | varchar | 注文名 (`#1001`) |
| 顧客ID | customer_id | varchar | 顧客 ID (FK、ゲストは null) |
| 支払ステータス / 配送ステータス | financial_status / fulfillment_status | varchar | 支払 / 配送ステータス |
| 注文チャネル | source_name | varchar | 注文チャネル |
| 通貨コード | currency_code | varchar | 通貨 |
| メールアドレス / 電話番号 / 備考 | email / phone / note | varchar | 連絡先・備考 |
| 配送先市区町村 / 配送先都道府県 / 配送先国 / 配送先国コード / 配送先郵便番号 | ship_city / ship_province / ship_country / ship_country_code / ship_zip | varchar | 配送先 |
| 合計金額 / 小計 / 税額 / 割引総額 / 送料 | total_price / subtotal_price / total_tax / total_discounts / total_shipping | double | 各金額 (作成時点) |
| 現在合計金額 | current_total_price | double | 返金反映後の現在合計 |
| 返金総額 | total_refunded | double | 返金総額 |
| 作成日時 / 更新日時 / 処理日時 / キャンセル日時 / クローズ日時 | created_at / updated_at / processed_at / cancelled_at / closed_at | timestamp | 各日時 |
| 注文dlt行ID | order_dlt_id | varchar | inline list 子 (discount_codes) 結合用 dlt 行 ID |
