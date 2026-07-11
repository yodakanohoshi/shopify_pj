# intermediate.int_discounts__enriched

割引 + コード利用集計 + 注文適用実績。粒度: 1 行 = 1 割引。

| カラム | 型 | 説明 |
|---|---|---|
| discount_id | varchar | 割引 ID。**PK** |
| discount_type / discount_method | varchar | 種別 / 手法 |
| discount_title / discount_status | varchar | 名称 / 状態 |
| discount_percentage / discount_amount / discount_currency | double / varchar | 割引値 |
| usage_limit | integer | 利用上限 |
| total_usage_count | integer | 総利用回数 (API 値) |
| code_count / code_usage_total | integer | コード数 / コード利用合計 |
| sample_code | varchar | 代表コード |
| orders_with_code | integer | そのコードが使われた注文数 (実績) |
| starts_at / ends_at | timestamp | 有効期間 |

> `orders_with_code` は注文の適用コード文字列 (`stg_shopify__order_discount_codes`) を
> 割引コード (`stg_shopify__discount_codes`) と突合した実績値。
