# staging.stg_shopify__order_refunds

注文の返金。元: `raw.orders__refunds` (orders の inline list `refunds` を dlt が正規化)。粒度: 1 行 = 1 返金。order_dlt_id で `stg_shopify__orders.order_dlt_id` に紐づく。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 返金ID | refund_id | varchar | 返金の数値ID (gid から抽出)。**PK** |
| 注文dlt行ID | order_dlt_id | varchar | 親注文への結合キー。**FK → stg_shopify__orders.order_dlt_id** |
| メモ | note | varchar | 返金の任意メモ |
| 返金額 | refund_amount | double | 全取引の返金合計額 |
| 通貨コード | currency_code | varchar | 返金額の通貨 |
| 作成日時 / 処理日時 | created_at / processed_at | timestamp | 返金作成日時 / 処理日時 |
