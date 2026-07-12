# raw.discounts__codes

割引コード。discounts の子テーブル (`codes` connection)。粒度: 1 行 = 1 コード。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| dlt行ID | _dlt_id | varchar | 行一意 ID。**PK** |
| dlt親行ID | _dlt_parent_id | varchar | 親割引の `discounts._dlt_id`。**FK** |
| コードID | id | varchar | コード global ID |
| 割引コード | code | varchar | 割引コード文字列 |
| 利用回数 | async_usage_count | bigint | コード別利用回数 |
