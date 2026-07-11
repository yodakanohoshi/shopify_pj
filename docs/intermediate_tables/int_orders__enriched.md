# intermediate.int_orders__enriched

注文 + 明細集計 + 顧客属性 + 返金反映後の純売上。粒度: 1 行 = 1 注文。

| カラム | 型 | 説明 |
|---|---|---|
| order_id | varchar | 注文 ID。**PK** |
| order_name / order_legacy_id | varchar | 注文名 / legacy ID |
| customer_id | varchar | 顧客 ID (FK) |
| customer_email / customer_country | varchar | 顧客付帯情報 (結合) |
| financial_status / fulfillment_status | varchar | ステータス |
| source_name | varchar | チャネル |
| currency_code | varchar | 通貨 |
| ship_country / ship_province / ship_city | varchar | 配送先 |
| total_price / subtotal_price / total_tax / total_discounts / total_shipping | double | 各金額 |
| total_refunded / current_total_price | double | 返金 / 返金反映後合計 |
| net_revenue | double | 純売上 = 小計 − 割引 − 返金 |
| discount_code_count / first_discount_code | integer / varchar | 適用コード数 / 代表コード |
| line_count / total_quantity / line_discount_total | integer / double | 明細集計 |
| order_date | date | 注文日 |
| is_cancelled / has_refund | boolean | キャンセル / 返金あり |
| created_at / processed_at / cancelled_at | timestamp | 各日時 |
