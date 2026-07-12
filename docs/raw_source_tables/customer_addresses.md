# raw.customer_addresses

顧客の住所。取得方式: **Bulk** (`customers.addressesV2`)。粒度: 1 行 = 1 住所。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 住所ID | id | varchar | 住所 global ID。**PK** |
| 親ID | parent_id | varchar | 親顧客の gid。**FK → customers.id** |
| 市区町村 / 都道府県 / 国 / 国コード / 郵便番号 | city / province / country / country_code_v2 / zip | varchar | 住所要素 |
