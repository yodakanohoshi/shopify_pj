# raw.locations

ロケーション (在庫/フルフィルメント拠点)。取得方式: **ページング** (`locations`)。
粒度: 1 行 = 1 拠点。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| ロケーションID | id | varchar | ロケーション global ID。**PK** |
| レガシーID | legacy_resource_id | varchar | 数値 legacy ID |
| ロケーション名 | name | varchar | 拠点名 |
| 有効フラグ | is_active | boolean | 有効か |
| オンライン注文対応 | fulfills_online_orders | boolean | オンライン注文を出荷するか |
| 市区町村 / 都道府県 / 国 / 国コード / 郵便番号 | address__city / __province / __country / __country_code / __zip | varchar | 拠点住所 |
