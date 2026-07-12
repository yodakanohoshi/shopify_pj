# marts.dim_locations

ロケーションディメンション (在庫/フルフィルメント拠点)。粒度: 1 行 = 1 拠点。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| ロケーションID | location_id | varchar | ロケーション ID。**PK** |
| ロケーションレガシーID | location_legacy_id | varchar | 数値 legacy ID |
| ロケーション名 | location_name | varchar | 拠点名 |
| 有効フラグ | is_active | boolean | 有効か |
| オンライン注文対応 | fulfills_online_orders | boolean | オンライン注文を出荷するか |
| 出荷可否 | ships_inventory | boolean | 出荷元指定 (レガシー) |
| 有効在庫有無 | has_active_inventory | boolean | 有効在庫を持つか |
| 住所1 / 住所2 | address1 / address2 | varchar | 住所の1行目 / 2行目 |
| 市区町村 / 都道府県 / 都道府県コード / 国 / 国コード / 郵便番号 | city / province / province_code / country / country_code / zip | varchar | 拠点住所 |
| 電話番号 | phone | varchar | ロケーション電話番号 |
| 緯度 / 経度 | latitude / longitude | double | 概算緯度 / 概算経度 |
