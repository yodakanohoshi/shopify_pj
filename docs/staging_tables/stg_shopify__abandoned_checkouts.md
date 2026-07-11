# staging.stg_shopify__abandoned_checkouts

放棄チェックアウト。元: `raw.abandoned_checkouts`。粒度: 1 行 = 1 チェックアウト。

| カラム | 型 | 説明 |
|---|---|---|
| checkout_id | varchar | チェックアウト ID。**PK** |
| customer_id | varchar | 顧客 ID (匿名は null) |
| abandoned_checkout_url | varchar | 復帰用 URL |
| total_price / subtotal_price | double | 合計 / 小計 |
| currency_code | varchar | 通貨 |
| created_at / updated_at / completed_at | timestamp | 各日時 |
| is_recovered | boolean | completed_at 非 null (後から購入=復帰) |
