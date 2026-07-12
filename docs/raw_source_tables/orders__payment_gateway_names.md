# raw.orders__payment_gateway_names

注文で使用された決済ゲートウェイ名。orders の inline list (`paymentGatewayNames`) を dlt が子テーブル化。
粒度: 1 行 = (注文 × ゲートウェイ名)。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| dlt行ID | _dlt_id | varchar | 行一意 ID。**PK** |
| dlt親行ID | _dlt_parent_id | varchar | 親注文の `orders._dlt_id`。**FK** |
| 決済GW名 | value | varchar | 使用決済ゲートウェイ名 |
