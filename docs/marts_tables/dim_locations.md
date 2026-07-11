# marts.dim_locations

ロケーションディメンション (在庫/フルフィルメント拠点)。粒度: 1 行 = 1 拠点。

| カラム | 型 | 説明 |
|---|---|---|
| location_id | varchar | ロケーション ID。**PK** |
| location_legacy_id | varchar | 数値 legacy ID |
| location_name | varchar | 拠点名 |
| is_active | boolean | 有効か |
| fulfills_online_orders | boolean | オンライン注文を出荷するか |
| city / province / country / country_code / zip | varchar | 拠点住所 |
