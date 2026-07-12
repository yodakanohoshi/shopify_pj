# staging.stg_shopify__customer_addresses

顧客住所。元: `raw.customer_addresses`。粒度: 1 行 = 1 住所。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 住所ID | address_id | varchar | 住所 ID。**PK** |
| 顧客ID | customer_id | varchar | 顧客 ID。**FK → stg_shopify__customers.customer_id** |
| 市区町村 / 都道府県 / 国 / 国コード / 郵便番号 | city / province / country / country_code / zip | varchar | 住所要素 |
