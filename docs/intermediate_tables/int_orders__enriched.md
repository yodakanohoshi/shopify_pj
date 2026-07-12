# intermediate.int_orders__enriched

注文 + 明細集計 + 顧客属性 + 返金反映後の純売上。粒度: 1 行 = 1 注文。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 注文ID | order_id | varchar | 注文 ID。**PK** |
| 注文名 / 注文レガシーID | order_name / order_legacy_id | varchar | 注文名 / legacy ID |
| 顧客ID | customer_id | varchar | 顧客 ID (FK) |
| 顧客メールアドレス / 顧客国 | customer_email / customer_country | varchar | 顧客付帯情報 (結合) |
| 支払ステータス / 配送ステータス | financial_status / fulfillment_status | varchar | ステータス |
| 注文チャネル | source_name | varchar | チャネル |
| 通貨コード | currency_code | varchar | 通貨 |
| 配送先国 / 配送先都道府県 / 配送先市区町村 | ship_country / ship_province / ship_city | varchar | 配送先 |
| 合計金額 / 小計 / 税額 / 割引総額 / 送料 | total_price / subtotal_price / total_tax / total_discounts / total_shipping | double | 各金額 |
| 返金総額 / 現在合計金額 | total_refunded / current_total_price | double | 返金 / 返金反映後合計 |
| 純売上 | net_revenue | double | 純売上 = 小計 − 割引 − 返金 |
| 適用コード数 / 代表割引コード | discount_code_count / first_discount_code | integer / varchar | 適用コード数 / 代表コード |
| 明細数 / 合計数量 / 明細割引額 | line_count / total_quantity / line_discount_total | integer / double | 明細集計 |
| 注文日 | order_date | date | 注文日 |
| キャンセル済み / 返金あり | is_cancelled / has_refund | boolean | キャンセル / 返金あり |
| 作成日時 / 処理日時 / キャンセル日時 | created_at / processed_at / cancelled_at | timestamp | 各日時 |
