# raw.customers__tags

顧客タグ。customers の inline scalar list (`tags: [String!]!`) を dlt が子テーブル化。
粒度: 1 行 = (顧客 × タグ)。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| dlt行ID | _dlt_id | varchar | 行一意 ID。**PK** |
| dlt親行ID | _dlt_parent_id | varchar | 親顧客の `customers._dlt_id`。**FK** |
| タグ | value | varchar | タグ文字列 (1 タグ = 1 行) |
