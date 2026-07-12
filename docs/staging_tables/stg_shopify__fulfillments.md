# staging.stg_shopify__fulfillments

注文のフルフィルメント (出荷)。元: `raw.orders__fulfillments` (orders の inline list `fulfillments` を dlt が正規化)。粒度: 1 行 = 1 出荷。order_dlt_id で `stg_shopify__orders.order_dlt_id` に紐づく。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 出荷ID | fulfillment_id | varchar | フルフィルメントの数値ID (gid から抽出)。**PK** |
| 注文dlt行ID | order_dlt_id | varchar | 親注文への結合キー。**FK → stg_shopify__orders.order_dlt_id** |
| 出荷名 | fulfillment_name | varchar | 出荷の参照識別子 |
| 出荷ステータス | fulfillment_status | varchar | 出荷の状態 |
| 表示ステータス | display_status | varchar | 人間可読の表示ステータス |
| 合計数量 | total_quantity | integer | 全明細の数量合計 |
| 作成日時 / 更新日時 | created_at / updated_at | timestamp | 出荷作成日時 / 最終更新日時 |
| 到着予定 | estimated_delivery_at | timestamp | 配達予定日 |
| 輸送開始日 | in_transit_at | timestamp | 輸送に入った日時 |
| 配達日 | delivered_at | timestamp | 配達完了日 |
