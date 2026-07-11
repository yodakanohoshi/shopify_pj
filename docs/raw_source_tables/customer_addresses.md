# raw.customer_addresses

顧客の住所。取得方式: **Bulk** (`customers.addressesV2`)。粒度: 1 行 = 1 住所。

| カラム | 型 | 説明 |
|---|---|---|
| id | varchar | 住所 global ID。**PK** |
| parent_id | varchar | 親顧客の gid。**FK → customers.id** |
| city / province / country / country_code_v2 / zip | varchar | 住所要素 |
