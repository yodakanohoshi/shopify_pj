# marts.fct_refunds

返金ファクト。返金額・返金日・注文/顧客の分析基点。注文粒度の total_refunded を裏付ける明細。粒度: 1 行 = 1 返金。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 返金ID | refund_id | varchar | 数値ID (gid から抽出)。**PK** |
| 注文ID | order_id | varchar | 数値ID (gid から抽出)。**FK → fct_orders** |
| 顧客ID | customer_id | varchar | 数値ID (gid から抽出)。**FK → dim_customers** (ゲストは null) |
| 返金日 | refund_date | date | 返金日 (created_at の日付) |
| 返金額 | refund_amount | double | 全取引の返金合計額 |
| 通貨コード | currency_code | varchar | 返金額の通貨 |
| メモ | note | varchar | 返金の任意メモ |
| 作成日時 / 処理日時 | created_at / processed_at | timestamp | 返金の作成 / 処理日時 |
