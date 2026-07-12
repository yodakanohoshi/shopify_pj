# staging.stg_shopify__discounts

割引 (コード割引 + 自動割引)。元: `raw.discounts`。粒度: 1 行 = 1 割引。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 割引ID | discount_id | varchar | 割引 ID。**PK** |
| 割引タイプ | discount_type | varchar | Shopify 種別名 |
| 割引方式 | discount_method | varchar | `code` / `automatic` / `other` (種別から判定) |
| 割引名 | discount_title | varchar | 割引名 |
| ステータス | discount_status | varchar | ACTIVE / EXPIRED / SCHEDULED |
| 概要 | summary | varchar | 内容要約 |
| 利用上限 | usage_limit | integer | 利用上限 |
| 顧客あたり1回限定 | applies_once_per_customer | boolean | 顧客あたり1回制限 |
| 利用回数 | total_usage_count | integer | 総利用回数 |
| 割引率 / 割引額 / 通貨コード | discount_percentage / discount_amount / discount_currency | double / varchar | 割引値 (定率 / 定額) |
| 開始日時 / 終了日時 | starts_at / ends_at | timestamp | 有効期間 |
| 割引dlt行ID | discount_dlt_id | varchar | コード子テーブル結合用 dlt 行 ID |
