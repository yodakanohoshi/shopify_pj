# intermediate.int_customers__enriched

顧客 + 実注文集計 + 配信同意 + セグメント。粒度: 1 行 = 1 顧客。

| カラム | 型 | 説明 |
|---|---|---|
| customer_id | varchar | 顧客 ID。**PK** |
| customer_legacy_id | varchar | legacy ID |
| first_name / last_name / email | varchar | 氏名・メール |
| email_marketing_state / email_marketing_opt_in_level | varchar | 配信同意 |
| is_email_subscribed | boolean | 配信可能 (state = SUBSCRIBED) |
| customer_state | varchar | 顧客状態 |
| country / country_code / city | varchar | 所在地 |
| lifetime_amount_spent | double | 生涯購入額 (API 値) |
| orders_count / revenue_total / avg_order_value | integer / double | 実注文集計 (キャンセル除く) |
| address_count | integer | 登録住所数 |
| customer_segment | varchar | prospect / one_time / repeat / loyal |
| first_order_date / latest_order_date | date | 初回 / 最新注文日 |
| created_at / updated_at | timestamp | 各日時 |
