# staging.stg_shopify__customers

顧客マスタ。元: `raw.customers`。粒度: 1 行 = 1 顧客。

| カラム | 型 | 説明 |
|---|---|---|
| customer_id | varchar | 顧客 ID。**PK** |
| customer_legacy_id | varchar | 数値 legacy ID |
| first_name / last_name / email / phone | varchar | 氏名・連絡先 |
| email_marketing_state | varchar | メール配信同意 (SUBSCRIBED 等) |
| email_marketing_opt_in_level | varchar | オプトインレベル |
| verified_email | boolean | メール確認済みか |
| customer_state | varchar | 顧客状態 |
| number_of_orders | integer | 注文数 (API 集計値) |
| lifetime_amount_spent / amount_spent_currency | double / varchar | 生涯購入額 / 通貨 |
| city / province / country / country_code / zip | varchar | 既定住所 |
| note | varchar | 備考 |
| created_at / updated_at | timestamp | 各日時 |
