# raw.abandoned_checkouts

放棄チェックアウト (カゴ落ち)。取得方式: **Bulk** (`abandonedCheckouts`)。
dlt 標準非対応をカスタム取得。粒度: 1 行 = 1 チェックアウト。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| カゴ落ちID | id | varchar | チェックアウト global ID。**PK** |
| 顧客ID | customer__id | varchar | 顧客 ID (FK → customers.id、匿名は null) |
| カゴ落ちURL | abandoned_checkout_url | varchar | 復帰用 URL |
| 合計金額 / 通貨コード | total_price_set__shop_money__amount / __currency_code | varchar | 合計金額 / 通貨 |
| 小計 | subtotal_price_set__shop_money__amount | varchar(数値) | 小計 |
| 作成日時 / 更新日時 | created_at / updated_at | varchar(ISO8601) | 各日時 |
| 完了日時 | completed_at | varchar(ISO8601) | 完了日時 (非 null は後から購入=復帰) |

子テーブル: [abandoned_checkout_line_items](abandoned_checkout_line_items.md) (parent_id → id)。
