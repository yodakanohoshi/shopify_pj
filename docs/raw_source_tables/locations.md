# raw.locations

ロケーション (在庫/フルフィルメント拠点)。取得方式: **ページング** (`locations`)。
粒度: 1 行 = 1 拠点。

| カラム | 型 | 説明 |
|---|---|---|
| id | varchar | ロケーション global ID。**PK** |
| legacy_resource_id | varchar | 数値 legacy ID |
| name | varchar | 拠点名 |
| is_active | boolean | 有効か |
| fulfills_online_orders | boolean | オンライン注文を出荷するか |
| address__city / __province / __country / __country_code / __zip | varchar | 拠点住所 |
