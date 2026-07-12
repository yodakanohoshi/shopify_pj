# marts.fct_order_transactions

決済取引ファクト。決済ゲートウェイ別売上・入金・返金の分析基点。粒度: 1 行 = 1 取引 (authorization / capture / sale / refund / void)。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 取引ID | transaction_id | varchar | 取引 ID。**PK** |
| 注文ID | order_id | varchar | 注文 ID。**FK → fct_orders** |
| 顧客ID | customer_id | varchar | 顧客 ID。**FK → dim_customers** (ゲストは null) |
| 取引種別 | transaction_kind | varchar | authorization / capture / sale / refund / void 等 |
| 取引ステータス | transaction_status | varchar | SUCCESS / FAILURE / PENDING 等 |
| 決済GW | gateway | varchar | 使用決済ゲートウェイ |
| テスト取引 | is_test | boolean | テスト取引か |
| 取引金額 | amount | double | 取引の金額 |
| 通貨コード | currency_code | varchar | 取引金額の通貨 |
| 取引日 | transaction_date | date | 取引日 (processed_at の日付) |
| 作成日時 / 処理日時 | created_at / processed_at | timestamp | 取引の作成 / 処理日時 |
