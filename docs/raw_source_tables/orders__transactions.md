# raw.orders__transactions

注文の決済取引。orders の inline list (`transactions`) を dlt が子テーブル化。
取得方式: **Bulk**。粒度: 1 行 = 1 取引。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 取引ID | id | varchar | 取引 global ID。**PK** |
| dlt親行ID | _dlt_parent_id | varchar | 親注文の `orders._dlt_id`。**FK** |
| 取引種別 | kind | varchar | authorization/capture/sale/refund/void 等 |
| 取引ステータス | status | varchar | SUCCESS/FAILURE/PENDING 等 |
| 決済GW | gateway | varchar | 使用決済ゲートウェイ |
| テスト取引 | test | boolean | テスト取引か |
| 処理日時 / 作成日時 | processed_at / created_at | varchar(ISO8601) | 取引処理 / 作成日時 |
| 取引金額 | amount_set__shop_money__amount | varchar(数値) | 取引の金額 |
| 通貨コード | amount_set__shop_money__currency_code | varchar | 取引金額の通貨 |

親子関係: `_dlt_parent_id` → [orders](orders.md)`._dlt_id`。
