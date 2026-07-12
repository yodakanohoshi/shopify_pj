# marts.fct_fulfillments

フルフィルメント (出荷) ファクト。配送リードタイム・出荷状況の分析基点。粒度: 1 行 = 1 出荷。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 出荷ID | fulfillment_id | varchar | 数値ID (gid から抽出)。**PK** |
| 注文ID | order_id | varchar | 数値ID (gid から抽出)。**FK → fct_orders** |
| 顧客ID | customer_id | varchar | 数値ID (gid から抽出)。**FK → dim_customers** (ゲストは null) |
| 出荷名 | fulfillment_name | varchar | 出荷の参照識別子 |
| 出荷ステータス | fulfillment_status | varchar | 出荷の状態 |
| 表示ステータス | display_status | varchar | 人間可読の表示ステータス |
| 合計数量 | total_quantity | integer | 全明細の数量合計 |
| 出荷日 | fulfilled_date | date | 出荷日 (created_at の日付) |
| 作成日時 / 更新日時 | created_at / updated_at | timestamp | 出荷の作成 / 最終更新日時 |
| 到着予定 | estimated_delivery_at | timestamp | 配達予定日時 |
| 輸送開始日 | in_transit_at | timestamp | 輸送に入った日時 |
| 配達日 | delivered_at | timestamp | 配達完了日時 |
| 出荷所要日数 | days_to_fulfill | integer | 受注から出荷までの日数 |
