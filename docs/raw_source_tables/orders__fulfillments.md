# raw.orders__fulfillments

注文のフルフィルメント (出荷)。orders の inline list (`fulfillments`) を dlt が子テーブル化。
取得方式: **Bulk**。粒度: 1 行 = 1 出荷。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 出荷ID | id | varchar | フルフィルメント global ID。**PK** |
| dlt親行ID | _dlt_parent_id | varchar | 親注文の `orders._dlt_id`。**FK** |
| 出荷ステータス | status | varchar | 出荷の状態 |
| 表示ステータス | display_status | varchar | 人間可読の表示ステータス |
| 出荷名 | name | varchar | 出荷の参照識別子 |
| 合計数量 | total_quantity | varchar(数値) | 全明細の数量合計 |
| 作成日時 / 更新日時 | created_at / updated_at | varchar(ISO8601) | 出荷作成 / 最終更新日時 |
| 到着予定 | estimated_delivery_at | varchar(ISO8601) | 配達予定日 |
| 輸送開始日 | in_transit_at | varchar(ISO8601) | 輸送に入った日時 |
| 配達日 | delivered_at | varchar(ISO8601) | 配達完了日 |

親子関係: `_dlt_parent_id` → [orders](orders.md)`._dlt_id`。
