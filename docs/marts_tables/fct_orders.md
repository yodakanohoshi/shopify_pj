# marts.fct_orders

注文ファクト。売上・返金・チャネル・地理の分析基点。粒度: 1 行 = 1 注文。

| カラム | 型 | 説明 |
|---|---|---|
| order_id | varchar | 注文 ID。**PK** |
| order_name | varchar | 注文名 |
| customer_id | varchar | 顧客 ID。**FK → dim_customers** (ゲストは null) |
| order_date | date | 注文日 |
| source_name | varchar | チャネル |
| financial_status / fulfillment_status | varchar | ステータス |
| is_cancelled / has_refund | boolean | キャンセル / 返金あり |
| currency_code | varchar | 通貨 |
| ship_country / ship_province | varchar | 配送先 |
| line_count / total_quantity | integer | 明細数 / 合計数量 |
| discount_code_count / first_discount_code | integer / varchar | 適用コード数 / 代表コード |
| subtotal_price / total_discounts / total_tax / total_shipping / total_refunded / total_price | double | 各金額 |
| current_total_price | double | 返金反映後合計 |
| net_revenue | double | 純売上 = 小計 − 割引 − 返金 |
| created_at / processed_at | timestamp | 各日時 |
