# raw.orders__discount_codes

注文に適用された割引コード文字列。orders の inline list (`discountCodes`) を dlt が子テーブル化。
粒度: 1 行 = (注文 × コード)。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| dlt行ID | _dlt_id | varchar | 行一意 ID。**PK** |
| dlt親行ID | _dlt_parent_id | varchar | 親注文の `orders._dlt_id`。**FK** |
| 割引コード | value | varchar | 割引コード文字列 |
