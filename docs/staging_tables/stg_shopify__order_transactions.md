# staging.stg_shopify__order_transactions

注文の決済取引。元: `raw.orders__transactions` (orders の inline list `transactions` を dlt が正規化)。粒度: 1 行 = 1 取引 (authorization / capture / refund / sale 等)。order_dlt_id で `stg_shopify__orders.order_dlt_id` に紐づく。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 取引ID | transaction_id | varchar | 取引の数値ID (gid から抽出)。**PK** |
| 注文dlt行ID | order_dlt_id | varchar | 親注文への結合キー。**FK → stg_shopify__orders.order_dlt_id** |
| 取引種別 | transaction_kind | varchar | authorization / capture / sale / refund / void 等 |
| 取引ステータス | transaction_status | varchar | SUCCESS / FAILURE / PENDING 等 |
| 決済GW | gateway | varchar | 使用決済ゲートウェイ |
| テスト取引 | is_test | boolean | テスト取引か |
| 取引金額 | amount | double | 取引の金額 |
| 通貨コード | currency_code | varchar | 取引金額の通貨 |
| 作成日時 / 処理日時 | created_at / processed_at | timestamp | 取引作成日時 / 処理日時 |
