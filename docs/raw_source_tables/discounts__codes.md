# raw.discounts__codes

割引コード。discounts の子テーブル (`codes` connection)。粒度: 1 行 = 1 コード。

| カラム | 型 | 説明 |
|---|---|---|
| _dlt_id | varchar | 行一意 ID。**PK** |
| _dlt_parent_id | varchar | 親割引の `discounts._dlt_id`。**FK** |
| id | varchar | コード global ID |
| code | varchar | 割引コード文字列 |
| async_usage_count | bigint | コード別利用回数 |
