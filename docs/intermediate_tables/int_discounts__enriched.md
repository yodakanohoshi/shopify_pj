# intermediate.int_discounts__enriched

割引 + コード利用集計 + 注文適用実績。粒度: 1 行 = 1 割引。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 割引ID | discount_id | varchar | 数値ID (gid から抽出)。**PK** |
| 割引タイプ / 割引方式 | discount_type / discount_method | varchar | 種別 / 手法 |
| 割引名 / ステータス | discount_title / discount_status | varchar | 名称 / 状態 |
| 割引率 / 割引額 / 通貨コード | discount_percentage / discount_amount / discount_currency | double / varchar | 割引値 |
| 利用上限 | usage_limit | integer | 利用上限 |
| 総利用回数 | total_usage_count | integer | 総利用回数 (API 値) |
| コード数 / コード利用合計 | code_count / code_usage_total | integer | コード数 / コード利用合計 |
| 代表割引コード | sample_code | varchar | 代表コード |
| 適用注文数 | orders_with_code | integer | そのコードが使われた注文数 (実績) |
| 開始日時 / 終了日時 | starts_at / ends_at | timestamp | 有効期間 |

> `orders_with_code` は注文の適用コード文字列 (`stg_shopify__order_discount_codes`) を
> 割引コード (`stg_shopify__discount_codes`) と突合した実績値。
