# raw.orders

注文ヘッダ。取得方式: **Bulk** (`orders`)。粒度: 1 行 = 1 注文。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 注文ID | id | varchar | 注文 global ID (`gid://shopify/Order/...`)。**PK** |
| 注文レガシーID | legacy_resource_id | varchar | 数値の legacy 注文 ID |
| 注文名 | name | varchar | 注文名 (例 `#1001`) |
| 注文番号 | number | varchar(数値) | プレフィクス除く連番 (非一意) |
| 確認番号 | confirmation_number | varchar | 顧客向けランダム識別子 (非一意) |
| 作成日時 / 更新日時 | created_at / updated_at | varchar(ISO8601) | 作成 / 更新日時 |
| 処理日時 / キャンセル日時 / クローズ日時 | processed_at / cancelled_at / closed_at | varchar | 処理 / キャンセル / クローズ日時 |
| キャンセル理由 | cancel_reason | varchar | 注文キャンセルの理由。未キャンセルは null |
| クローズ済 | closed | boolean | 全項目完了で注文が閉じたか |
| テスト注文 | test | boolean | テスト注文か |
| 税込フラグ | taxes_included | boolean | 小計に税が含まれるか |
| 免税 | tax_exempt | boolean | 注文が免税か |
| 支払ステータス | display_financial_status | varchar | 支払ステータス (PAID, PENDING, REFUNDED 等) |
| 配送ステータス | display_fulfillment_status | varchar | 配送ステータス (FULFILLED, UNFULFILLED 等) |
| 通貨コード | currency_code | varchar | 通貨コード |
| 注文チャネル | source_name | varchar | 注文チャネル (web, pos, mobile_app 等) |
| メールアドレス / 電話番号 / 備考 | email / phone / note | varchar | 連絡先・備考 |
| PO番号 | po_number | varchar | 発注番号 (B2B) |
| 顧客ロケール | customer_locale | varchar | 購入時の言語地域 (例 en, fr-CA) |
| マーケ同意 | customer_accepts_marketing | boolean | 購入時のマーケメール受信同意 |
| タグ | tags | (子: orders__tags) | タグ (inline list) |
| 割引コード | discount_codes | (子: orders__discount_codes) | 適用割引コード文字列 (inline list) |
| 割引コード(代表) | discount_code | varchar | 使用した割引コード (単一)。無しは null |
| 決済GW名 | payment_gateway_names | (子: orders__payment_gateway_names) | 使用決済ゲートウェイ名 (inline list) |
| 顧客ID | customer__id | varchar | 注文者顧客 ID (FK → customers.id、ゲストは null) |
| 請求=配送一致 | billing_address_matches_shipping_address | boolean | 請求先と配送先が一致するか |
| 配送先市区町村 / 配送先都道府県 / 配送先国 / 配送先国コード / 配送先郵便番号 | shipping_address__city / __province / __country / __country_code_v2 / __zip | varchar | 配送先住所 |
| 請求先市区町村 / 請求先都道府県 / 請求先国 / 請求先国コード / 請求先郵便番号 | billing_address__city / __province / __country / __country_code_v2 / __zip | varchar | 請求先住所 |
| 小計対象数量 | subtotal_line_items_quantity | varchar(数値) | 小計に寄与する商品の合計数量 |
| 現小計対象数量 | current_subtotal_line_items_quantity | varchar(数値) | 返品等後の小計対象数量 |
| 現重量 | current_total_weight | varchar(数値) | 返品後の合計重量 (g) |
| 出荷件数 | fulfillments_count__count | varchar(数値) | キャンセル含む出荷総数 |
| 合計金額 | total_price_set__shop_money__amount | varchar(数値) | 合計金額 (作成時点) |
| 小計 | subtotal_price_set__shop_money__amount | varchar(数値) | 小計 |
| 現小計金額 | current_subtotal_price_set__shop_money__amount | varchar(数値) | 返品後の小計 (税割引込) |
| 現在合計金額 | current_total_price_set__shop_money__amount | varchar(数値) | 返金反映後の現在合計 |
| 税額 | total_tax_set__shop_money__amount | varchar(数値) | 税額 |
| 現税額合計 | current_total_tax_set__shop_money__amount | varchar(数値) | 返品後の税合計 |
| 割引総額 | total_discounts_set__shop_money__amount | varchar(数値) | 割引総額 |
| 現割引合計 | current_total_discounts_set__shop_money__amount | varchar(数値) | 返品後の割引合計 |
| 送料 | total_shipping_price_set__shop_money__amount | varchar(数値) | 送料 |
| 返金総額 | total_refunded_set__shop_money__amount | varchar(数値) | 返金総額 |
| 純支払額 | net_payment_set__shop_money__amount | varchar(数値) | 受領額 − 返金額 |

子テーブル: [order_line_items](order_line_items.md) (parent_id → id)、[orders__discount_codes](orders__discount_codes.md)、[orders__payment_gateway_names](orders__payment_gateway_names.md)、[orders__refunds](orders__refunds.md)、[orders__fulfillments](orders__fulfillments.md)、[orders__transactions](orders__transactions.md) (いずれも _dlt_parent_id → _dlt_id)。
