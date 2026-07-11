# staging.stg_shopify__customer_addresses

顧客住所。元: `raw.customer_addresses`。粒度: 1 行 = 1 住所。

| カラム | 型 | 説明 |
|---|---|---|
| address_id | varchar | 住所 ID。**PK** |
| customer_id | varchar | 顧客 ID。**FK → stg_shopify__customers.customer_id** |
| city / province / country / country_code / zip | varchar | 住所要素 |
