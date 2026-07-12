# marts.dim_customers

顧客ディメンション。属性 + 実注文集計 + 配信同意 + セグメント。粒度: 1 行 = 1 顧客。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 顧客ID | customer_id | varchar | 数値ID (gid から抽出)。**PK** |
| 顧客レガシーID | customer_legacy_id | varchar | 数値 legacy ID |
| 名 / 姓 / メールアドレス | first_name / last_name / email | varchar | 氏名・メール |
| メール配信可能 | is_email_subscribed | boolean | メール配信可能か |
| メール配信同意状態 | email_marketing_state | varchar | 配信同意状態 |
| 顧客状態 | customer_state | varchar | 顧客状態 |
| 顧客セグメント | customer_segment | varchar | prospect / one_time / repeat / loyal |
| 免税フラグ | tax_exempt | boolean | 注文で課税免除されるか |
| 顧客ロケール | customer_locale | varchar | 顧客の言語/地域設定 |
| 登録経過期間 | lifetime_duration | varchar | 初回登録からの経過 (例 about 2 years) |
| 国 / 国コード / 市区町村 | country / country_code / city | varchar | 所在地 |
| 生涯購入額 | lifetime_amount_spent | double | 生涯購入額 (API 値) |
| 注文数 / 売上合計 / 平均注文額 | orders_count / revenue_total / avg_order_value | integer / double | 実注文集計 (キャンセル除く) |
| 登録住所数 | address_count | integer | 登録住所数 |
| 初回注文日 / 最新注文日 | first_order_date / latest_order_date | date | 初回 / 最新注文日 |
| 作成日時 / 更新日時 | created_at / updated_at | timestamp | 各日時 |
