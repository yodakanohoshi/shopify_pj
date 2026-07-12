# raw.customers

顧客。取得方式: **Bulk** (`customers`)。粒度: 1 行 = 1 顧客。

> `email` / `emailMarketingConsent` は Admin API で非推奨のため `defaultEmailAddress` を使用。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 顧客ID | id | varchar | 顧客 global ID。**PK** |
| 顧客レガシーID | legacy_resource_id | varchar | 数値 legacy 顧客 ID |
| 名 / 姓 | first_name / last_name | varchar | 氏名 |
| メールアドレス | default_email_address__email_address | varchar | メールアドレス |
| メール配信同意状態 | default_email_address__marketing_state | varchar | メール配信同意 (SUBSCRIBED 等) |
| オプトインレベル | default_email_address__marketing_opt_in_level | varchar | オプトインレベル |
| 電話番号 | default_phone_number__phone_number | varchar | 電話番号 |
| メール確認済み | verified_email | boolean | メール確認済みか |
| 顧客状態 | state | varchar | 顧客状態 (ENABLED, DISABLED 等) |
| 注文数 | number_of_orders | bigint | 注文数 (API 集計値) |
| 生涯購入額 / 通貨コード | amount_spent__amount / __currency_code | varchar | 生涯購入額 / 通貨 |
| タグ | tags | (子: customers__tags) | タグ (inline list) |
| 備考 | note | varchar | 備考 |
| 既定住所市区町村 / 既定住所都道府県 / 既定住所国 / 既定住所国コード / 既定住所郵便番号 | default_address__city / __province / __country / __country_code_v2 / __zip | varchar | 既定住所 |
| 作成日時 / 更新日時 | created_at / updated_at | varchar(ISO8601) | 各日時 |

子テーブル: [customer_addresses](customer_addresses.md) (parent_id → id)。
