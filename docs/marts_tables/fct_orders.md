# marts.fct_orders

注文ファクト。売上・返金・チャネル・地理の分析基点。粒度: 1 行 = 1 注文。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 注文ID | order_id | varchar | 注文 ID。**PK** |
| 注文名 | order_name | varchar | 注文名 |
| 顧客ID | customer_id | varchar | 顧客 ID。**FK → dim_customers** (ゲストは null) |
| 注文日 | order_date | date | 注文日 |
| 注文チャネル | source_name | varchar | チャネル |
| 支払ステータス / 配送ステータス | financial_status / fulfillment_status | varchar | ステータス |
| キャンセル済み / 返金あり | is_cancelled / has_refund | boolean | キャンセル / 返金あり |
| 通貨コード | currency_code | varchar | 通貨 |
| 配送先国 / 配送先都道府県 | ship_country / ship_province | varchar | 配送先 |
| 明細数 / 合計数量 | line_count / total_quantity | integer | 明細数 / 合計数量 |
| 適用コード数 / 代表割引コード | discount_code_count / first_discount_code | integer / varchar | 適用コード数 / 代表コード |
| 小計 / 割引総額 / 税額 / 送料 / 返金総額 / 合計金額 | subtotal_price / total_discounts / total_tax / total_shipping / total_refunded / total_price | double | 各金額 |
| 現在合計金額 | current_total_price | double | 返金反映後合計 |
| 純売上 | net_revenue | double | 純売上 = 小計 − 割引 − 返金 |
| 作成日時 / 処理日時 | created_at / processed_at | timestamp | 各日時 |
