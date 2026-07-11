# staging.stg_shopify__discounts

割引 (コード割引 + 自動割引)。元: `raw.discounts`。粒度: 1 行 = 1 割引。

| カラム | 型 | 説明 |
|---|---|---|
| discount_id | varchar | 割引 ID。**PK** |
| discount_type | varchar | Shopify 種別名 |
| discount_method | varchar | `code` / `automatic` / `other` (種別から判定) |
| discount_title | varchar | 割引名 |
| discount_status | varchar | ACTIVE / EXPIRED / SCHEDULED |
| summary | varchar | 内容要約 |
| usage_limit | integer | 利用上限 |
| applies_once_per_customer | boolean | 顧客あたり1回制限 |
| total_usage_count | integer | 総利用回数 |
| discount_percentage / discount_amount / discount_currency | double / varchar | 割引値 (定率 / 定額) |
| starts_at / ends_at | timestamp | 有効期間 |
| discount_dlt_id | varchar | コード子テーブル結合用 dlt 行 ID |
