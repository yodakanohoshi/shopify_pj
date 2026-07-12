# marts.fct_discount_performance

割引パフォーマンスファクト。利用状況・適用注文数を評価。粒度: 1 行 = 1 割引。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 割引ID | discount_id | varchar | 数値ID (gid から抽出)。**PK** |
| 割引名 | discount_title | varchar | 割引名 |
| 割引タイプ / 割引方式 | discount_type / discount_method | varchar | 種別 / 手法 (code / automatic) |
| ステータス | discount_status | varchar | 状態 |
| 割引率 / 割引額 / 割引通貨 | discount_percentage / discount_amount / discount_currency | double / varchar | 割引値 |
| 利用上限 | usage_limit | integer | 利用上限 |
| 総利用回数 | total_usage_count | integer | 総利用回数 |
| コード数 / コード利用合計 | code_count / code_usage_total | integer | コード数 / コード利用合計 |
| 代表割引コード | sample_code | varchar | 代表コード |
| 適用注文数 | orders_with_code | integer | 適用注文数 (実績) |
| 利用上限消化率 | usage_ratio | double | 利用上限消化率 = total_usage_count / usage_limit |
| 開始日時 / 終了日時 | starts_at / ends_at | timestamp | 有効期間 |
