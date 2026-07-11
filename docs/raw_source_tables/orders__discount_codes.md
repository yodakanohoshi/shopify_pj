# raw.orders__discount_codes

注文に適用された割引コード文字列。orders の inline list (`discountCodes`) を dlt が子テーブル化。
粒度: 1 行 = (注文 × コード)。

| カラム | 型 | 説明 |
|---|---|---|
| _dlt_id | varchar | 行一意 ID。**PK** |
| _dlt_parent_id | varchar | 親注文の `orders._dlt_id`。**FK** |
| value | varchar | 割引コード文字列 |
