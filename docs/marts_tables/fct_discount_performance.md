# marts.fct_discount_performance

割引パフォーマンスファクト。利用状況・適用注文数を評価。粒度: 1 行 = 1 割引。

| カラム | 型 | 説明 |
|---|---|---|
| discount_id | varchar | 割引 ID。**PK** |
| discount_title | varchar | 割引名 |
| discount_type / discount_method | varchar | 種別 / 手法 (code / automatic) |
| discount_status | varchar | 状態 |
| discount_percentage / discount_amount / discount_currency | double / varchar | 割引値 |
| usage_limit | integer | 利用上限 |
| total_usage_count | integer | 総利用回数 |
| code_count / code_usage_total | integer | コード数 / コード利用合計 |
| sample_code | varchar | 代表コード |
| orders_with_code | integer | 適用注文数 (実績) |
| usage_ratio | double | 利用上限消化率 = total_usage_count / usage_limit |
| starts_at / ends_at | timestamp | 有効期間 |
