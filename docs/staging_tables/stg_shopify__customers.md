# staging.stg_shopify__customers

顧客マスタ。元: `raw.customers`。粒度: 1 行 = 1 顧客。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 顧客ID | customer_id | varchar | 顧客 ID。**PK** |
| 顧客レガシーID | customer_legacy_id | varchar | 数値 legacy ID |
| 名 / 姓 / メールアドレス / 電話番号 | first_name / last_name / email / phone | varchar | 氏名・連絡先 |
| メール配信同意状態 | email_marketing_state | varchar | メール配信同意 (SUBSCRIBED 等) |
| オプトインレベル | email_marketing_opt_in_level | varchar | オプトインレベル |
| メール確認済み | verified_email | boolean | メール確認済みか |
| 顧客状態 | customer_state | varchar | 顧客状態 |
| 免税フラグ | tax_exempt | boolean | 注文で課税免除されるか |
| 顧客ロケール | customer_locale | varchar | 顧客の言語/地域設定 |
| 登録経過期間 | lifetime_duration | varchar | 初回登録からの経過 (例 about 2 years) |
| 削除可否 | can_delete | boolean | 顧客を削除できるか |
| データ販売拒否 | data_sale_opt_out | boolean | データ販売をオプトアウト済か |
| 注文数 | number_of_orders | integer | 注文数 (API 集計値) |
| 生涯購入額 / 通貨コード | lifetime_amount_spent / amount_spent_currency | double / varchar | 生涯購入額 / 通貨 |
| 既定住所市区町村 / 既定住所都道府県 / 既定住所国 / 既定住所国コード / 既定住所郵便番号 | city / province / country / country_code / zip | varchar | 既定住所 |
| 備考 | note | varchar | 備考 |
| 作成日時 / 更新日時 | created_at / updated_at | timestamp | 各日時 |
