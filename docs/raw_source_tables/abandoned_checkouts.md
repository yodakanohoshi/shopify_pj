# raw.abandoned_checkouts

放棄チェックアウト (カゴ落ち)。取得方式: **Bulk** (`abandonedCheckouts`)。
dlt 標準非対応をカスタム取得。粒度: 1 行 = 1 チェックアウト。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| カゴ落ちID | id | varchar | チェックアウト global ID。**PK** |
| 顧客ID | customer__id | varchar | 顧客 ID (FK → customers.id、匿名は null) |
| カゴ落ちURL | abandoned_checkout_url | varchar | 復帰用 URL |
| メモ | note | varchar | 社内向けメモ |
| 税込フラグ | taxes_included | boolean | 価格に税を含むか |
| 割引コード | discount_codes | (子: abandoned_checkouts__discount_codes) | 入力された割引コード (inline list) |
| 請求先市区町村 / 請求先都道府県 / 請求先国 / 請求先国コード / 請求先郵便番号 | billing_address__city / __province / __country / __country_code_v2 / __zip | varchar | 請求先住所 |
| 配送先市区町村 / 配送先都道府県 / 配送先国 / 配送先国コード / 配送先郵便番号 | shipping_address__city / __province / __country / __country_code_v2 / __zip | varchar | 配送先住所 |
| 合計金額 / 通貨コード | total_price_set__shop_money__amount / __currency_code | varchar | 合計金額 / 通貨 |
| 小計 | subtotal_price_set__shop_money__amount | varchar(数値) | 小計 |
| 明細価格合計 | total_line_items_price_set__shop_money__amount | varchar(数値) | 全明細の価格合計 |
| 税額合計 | total_tax_set__shop_money__amount | varchar(数値) | チェックアウトの総税額 |
| 割引合計 | total_discount_set__shop_money__amount | varchar(数値) | 適用割引の総額 |
| 作成日時 / 更新日時 | created_at / updated_at | varchar(ISO8601) | 各日時 |
| 完了日時 | completed_at | varchar(ISO8601) | 完了日時 (非 null は後から購入=復帰) |

子テーブル: [abandoned_checkout_line_items](abandoned_checkout_line_items.md) (parent_id → id)、[abandoned_checkouts__discount_codes](abandoned_checkouts__discount_codes.md) (_dlt_parent_id → _dlt_id)。
