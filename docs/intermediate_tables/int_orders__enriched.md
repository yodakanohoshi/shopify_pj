# intermediate.int_orders__enriched

注文 + 明細集計 + 顧客属性 + 返金反映後の純売上。粒度: 1 行 = 1 注文。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 注文ID | order_id | varchar | 注文 ID。**PK** |
| 注文名 / 注文レガシーID | order_name / order_legacy_id | varchar | 注文名 / legacy ID |
| 顧客ID | customer_id | varchar | 顧客 ID (FK) |
| 顧客メールアドレス / 顧客国 | customer_email / customer_country | varchar | 顧客付帯情報 (結合) |
| 支払ステータス / 配送ステータス | financial_status / fulfillment_status | varchar | ステータス |
| キャンセル理由 | cancel_reason | varchar | キャンセルの理由 (未キャンセルは null) |
| 注文チャネル | source_name | varchar | チャネル |
| 通貨コード | currency_code | varchar | 通貨 |
| 確認番号 / PO番号 | confirmation_number / po_number | varchar | 顧客向け確認番号 / 発注番号 (B2B) |
| 顧客ロケール | customer_locale | varchar | 購入時の言語地域 |
| マーケ同意 / 税込フラグ / 免税 / テスト注文 | customer_accepts_marketing / taxes_included / tax_exempt / is_test | boolean | マーケメール同意 / 税込 / 免税 / テスト注文 |
| 配送先国 / 配送先都道府県 / 配送先市区町村 | ship_country / ship_province / ship_city | varchar | 配送先 |
| 合計金額 / 小計 / 税額 / 割引総額 / 送料 | total_price / subtotal_price / total_tax / total_discounts / total_shipping | double | 各金額 |
| 返金総額 / 現在合計金額 | total_refunded / current_total_price | double | 返金 / 返金反映後合計 |
| 純支払額 | net_payment | double | 純支払額 = 受領額 − 返金額 |
| 純売上 | net_revenue | double | 純売上 = 小計 − 割引 − 返金 |
| 適用コード数 / 代表割引コード | discount_code_count / first_discount_code | integer / varchar | 適用コード数 / 代表コード |
| 明細数 / 合計数量 / 明細割引額 | line_count / total_quantity / line_discount_total | integer / double | 明細集計 |
| 返金件数 / 返金額合計 | refund_count / refund_amount_total | integer / double | 返金集計 |
| 出荷件数 / 最終出荷日時 | fulfillment_count / last_fulfilled_at | integer / timestamp | 出荷集計 |
| 取引件数 / 入金額 | transaction_count / captured_amount | integer / double | 取引集計 (SUCCESS の SALE/CAPTURE 入金額) |
| 注文日 | order_date | date | 注文日 |
| キャンセル済み / 返金あり | is_cancelled / has_refund | boolean | キャンセル / 返金あり |
| 作成日時 / 処理日時 / キャンセル日時 | created_at / processed_at / cancelled_at | timestamp | 各日時 |
