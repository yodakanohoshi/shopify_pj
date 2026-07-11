# marts.fct_abandoned_checkouts

放棄チェックアウトファクト。カゴ落ち金額・復帰率などファネル分析に使う。
粒度: 1 行 = 1 チェックアウト。

| カラム | 型 | 説明 |
|---|---|---|
| checkout_id | varchar | チェックアウト ID。**PK** |
| customer_id | varchar | 顧客 ID (匿名は null) |
| checkout_date | date | 発生日 |
| currency_code | varchar | 通貨 |
| line_count / total_quantity | integer | 明細集計 |
| subtotal_price / total_price | double | 小計 / 合計 |
| is_recovered | boolean | 後から購入に至ったか (復帰) |
| created_at / completed_at | timestamp | 各日時 |
