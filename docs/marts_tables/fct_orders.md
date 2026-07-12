# marts.fct_orders

注文ファクト。売上・返金・チャネル・地理の分析基点。粒度: 1 行 = 1 注文。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 注文ID | order_id | varchar | 注文 ID。**PK** |
| 注文名 | order_name | varchar | 注文名 |
| 顧客ID | customer_id | varchar | 顧客 ID。**FK → dim_customers** (ゲストは null) |
| 注文日 | order_date | date | 注文日 |
| 注文チャネル | source_name | varchar | チャネル |
| 支払ステータス / 配送ステータス | financial_status / fulfillment_status | varchar | ステータス |
| キャンセル理由 | cancel_reason | varchar | 注文キャンセルの理由。未キャンセルは null |
| キャンセル済み / 返金あり | is_cancelled / has_refund | boolean | キャンセル / 返金あり |
| テスト注文 | is_test | boolean | テスト注文か |
| 税込フラグ | taxes_included | boolean | 小計に税が含まれるか |
| 免税 | tax_exempt | boolean | 注文が免税か |
| 確認番号 | confirmation_number | varchar | 顧客向けランダム識別子 (非一意) |
| PO番号 | po_number | varchar | 発注番号 (B2B) |
| 顧客ロケール | customer_locale | varchar | 購入時の言語地域 (例 en, fr-CA) |
| マーケ同意 | customer_accepts_marketing | boolean | 購入時のマーケメール受信同意 |
| 通貨コード | currency_code | varchar | 通貨 |
| 配送先国 / 配送先都道府県 | ship_country / ship_province | varchar | 配送先 |
| 明細数 / 合計数量 | line_count / total_quantity | integer | 明細数 / 合計数量 |
| 適用コード数 / 代表割引コード | discount_code_count / first_discount_code | integer / varchar | 適用コード数 / 代表コード |
| 返金件数 / 返金額合計 | refund_count / refund_amount_total | integer / double | 返金の件数 / 返金額合計 |
| 出荷件数 / 最終出荷日時 | fulfillment_count / last_fulfilled_at | integer / timestamp | 出荷の件数 / 最終出荷日時 |
| 取引件数 / 入金額 | transaction_count / captured_amount | integer / double | 決済取引の件数 / 入金額 |
| 小計 / 割引総額 / 税額 / 送料 / 返金総額 / 合計金額 | subtotal_price / total_discounts / total_tax / total_shipping / total_refunded / total_price | double | 各金額 |
| 現在合計金額 | current_total_price | double | 返金反映後合計 |
| 純支払額 | net_payment | double | 純支払額 = 受領額 − 返金額 |
| 純売上 | net_revenue | double | 純売上 = 小計 − 割引 − 返金 |
| 作成日時 / 処理日時 | created_at / processed_at | timestamp | 各日時 |
