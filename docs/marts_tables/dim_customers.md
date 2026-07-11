# marts.dim_customers

顧客ディメンション。属性 + 実注文集計 + 配信同意 + セグメント。粒度: 1 行 = 1 顧客。

| カラム | 型 | 説明 |
|---|---|---|
| customer_id | varchar | 顧客 ID。**PK** |
| customer_legacy_id | varchar | 数値 legacy ID |
| first_name / last_name / email | varchar | 氏名・メール |
| is_email_subscribed | boolean | メール配信可能か |
| email_marketing_state | varchar | 配信同意状態 |
| customer_state | varchar | 顧客状態 |
| customer_segment | varchar | prospect / one_time / repeat / loyal |
| country / country_code / city | varchar | 所在地 |
| lifetime_amount_spent | double | 生涯購入額 (API 値) |
| orders_count / revenue_total / avg_order_value | integer / double | 実注文集計 (キャンセル除く) |
| address_count | integer | 登録住所数 |
| first_order_date / latest_order_date | date | 初回 / 最新注文日 |
| created_at / updated_at | timestamp | 各日時 |
