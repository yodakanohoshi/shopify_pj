# raw.customers

顧客。取得方式: **Bulk** (`customers`)。粒度: 1 行 = 1 顧客。

> `email` / `emailMarketingConsent` は Admin API で非推奨のため `defaultEmailAddress` を使用。

| カラム | 型 | 説明 |
|---|---|---|
| id | varchar | 顧客 global ID。**PK** |
| legacy_resource_id | varchar | 数値 legacy 顧客 ID |
| first_name / last_name | varchar | 氏名 |
| default_email_address__email_address | varchar | メールアドレス |
| default_email_address__marketing_state | varchar | メール配信同意 (SUBSCRIBED 等) |
| default_email_address__marketing_opt_in_level | varchar | オプトインレベル |
| default_phone_number__phone_number | varchar | 電話番号 |
| verified_email | boolean | メール確認済みか |
| state | varchar | 顧客状態 (ENABLED, DISABLED 等) |
| number_of_orders | bigint | 注文数 (API 集計値) |
| amount_spent__amount / __currency_code | varchar | 生涯購入額 / 通貨 |
| tags | (子: customers__tags) | タグ (inline list) |
| note | varchar | 備考 |
| default_address__city / __province / __country / __country_code_v2 / __zip | varchar | 既定住所 |
| created_at / updated_at | varchar(ISO8601) | 各日時 |

子テーブル: [customer_addresses](customer_addresses.md) (parent_id → id)。
