# staging.stg_shopify__discount_codes

割引コード。元: `raw.discounts__codes`。粒度: 1 行 = 1 コード。

| カラム | 型 | 説明 |
|---|---|---|
| discount_code_id | varchar | コード ID。**PK** |
| discount_dlt_id | varchar | 親割引の dlt 行 ID。**FK → stg_shopify__discounts.discount_dlt_id** |
| discount_code | varchar | コード文字列 |
| code_usage_count | integer | コード別利用回数 |
