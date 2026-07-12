# staging.stg_shopify__discount_codes

割引コード。元: `raw.discounts__codes`。粒度: 1 行 = 1 コード。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 割引コードID | discount_code_id | varchar | コード ID。**PK** |
| 割引dlt行ID | discount_dlt_id | varchar | 親割引の dlt 行 ID。**FK → stg_shopify__discounts.discount_dlt_id** |
| 割引コード | discount_code | varchar | コード文字列 |
| コード別利用回数 | code_usage_count | integer | コード別利用回数 |
