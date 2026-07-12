# intermediate.int_customers__enriched

顧客 + 実注文集計 + 配信同意 + セグメント。粒度: 1 行 = 1 顧客。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 顧客ID | customer_id | varchar | 数値ID (gid から抽出)。**PK** |
| 顧客レガシーID | customer_legacy_id | varchar | legacy ID |
| 名 / 姓 / メールアドレス | first_name / last_name / email | varchar | 氏名・メール |
| メール配信同意状態 / オプトインレベル | email_marketing_state / email_marketing_opt_in_level | varchar | 配信同意 |
| メール配信可能 | is_email_subscribed | boolean | 配信可能 (state = SUBSCRIBED) |
| 顧客状態 | customer_state | varchar | 顧客状態 |
| 免税フラグ | tax_exempt | boolean | 注文で課税免除されるか |
| 顧客ロケール | customer_locale | varchar | 顧客の言語/地域設定 |
| 登録経過期間 | lifetime_duration | varchar | 初回登録からの経過 (例 about 2 years) |
| 国 / 国コード / 市区町村 | country / country_code / city | varchar | 所在地 |
| 生涯購入額 | lifetime_amount_spent | double | 生涯購入額 (API 値) |
| 注文数 / 売上合計 / 平均注文額 | orders_count / revenue_total / avg_order_value | integer / double | 実注文集計 (キャンセル除く) |
| 登録住所数 | address_count | integer | 登録住所数 |
| 顧客セグメント | customer_segment | varchar | prospect / one_time / repeat / loyal |
| タグ | tags | varchar | 顧客タグをカンマ連結 (明細は stg_shopify__customer_tags) |
| 初回注文日 / 最新注文日 | first_order_date / latest_order_date | date | 初回 / 最新注文日 |
| 作成日時 / 更新日時 | created_at / updated_at | timestamp | 各日時 |
