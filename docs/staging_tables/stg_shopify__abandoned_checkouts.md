# staging.stg_shopify__abandoned_checkouts

放棄チェックアウト。元: `raw.abandoned_checkouts`。粒度: 1 行 = 1 チェックアウト。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| カゴ落ちID | checkout_id | varchar | チェックアウト ID。**PK** |
| 顧客ID | customer_id | varchar | 顧客 ID (匿名は null) |
| カゴ落ちURL | abandoned_checkout_url | varchar | 復帰用 URL |
| 合計金額 / 小計 | total_price / subtotal_price | double | 合計 / 小計 |
| 通貨コード | currency_code | varchar | 通貨 |
| 作成日時 / 更新日時 / 完了日時 | created_at / updated_at / completed_at | timestamp | 各日時 |
| 復帰済み | is_recovered | boolean | completed_at 非 null (後から購入=復帰) |
