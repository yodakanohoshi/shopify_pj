# raw.orders__refunds

注文の返金。orders の inline list (`refunds`) を dlt が子テーブル化。
取得方式: **Bulk**。粒度: 1 行 = 1 返金。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 返金ID | id | varchar | 返金 global ID。**PK** |
| dlt親行ID | _dlt_parent_id | varchar | 親注文の `orders._dlt_id`。**FK** |
| 作成日時 | created_at | varchar(ISO8601) | 返金作成日時 |
| 処理日時 | processed_at | varchar(ISO8601) | 返金処理日時 |
| メモ | note | varchar | 返金の任意メモ |
| 返金合計 | total_refunded_set__shop_money__amount | varchar(数値) | 全取引の返金合計額 |
| 通貨コード | total_refunded_set__shop_money__currency_code | varchar | 返金額の通貨 |

親子関係: `_dlt_parent_id` → [orders](orders.md)`._dlt_id`。
