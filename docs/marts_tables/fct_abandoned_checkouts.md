# marts.fct_abandoned_checkouts

放棄チェックアウトファクト。カゴ落ち金額・復帰率などファネル分析に使う。
粒度: 1 行 = 1 チェックアウト。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| カゴ落ちID | checkout_id | varchar | チェックアウト ID。**PK** |
| 顧客ID | customer_id | varchar | 顧客 ID (匿名は null) |
| カゴ落ち日 | checkout_date | date | 発生日 |
| 通貨コード | currency_code | varchar | 通貨 |
| 明細数 / 合計数量 | line_count / total_quantity | integer | 明細集計 |
| 小計 / 合計金額 | subtotal_price / total_price | double | 小計 / 合計 |
| 復帰済み | is_recovered | boolean | 後から購入に至ったか (復帰) |
| 作成日時 / 完了日時 | created_at / completed_at | timestamp | 各日時 |
