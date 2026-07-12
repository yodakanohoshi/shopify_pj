# staging.stg_shopify__orders

注文ヘッダ (クレンジング済み)。元: `raw.orders`。粒度: 1 行 = 1 注文。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 注文ID | order_id | varchar | 注文 ID。**PK** |
| 注文レガシーID | order_legacy_id | varchar | 数値 legacy 注文 ID |
| 注文名 | order_name | varchar | 注文名 (`#1001`) |
| 注文番号 | order_number | integer | プレフィクス除く連番 (非一意) |
| 確認番号 | confirmation_number | varchar | 顧客向けランダム識別子 (非一意) |
| 顧客ID | customer_id | varchar | 顧客 ID (FK、ゲストは null) |
| 支払ステータス / 配送ステータス | financial_status / fulfillment_status | varchar | 支払 / 配送ステータス |
| キャンセル理由 | cancel_reason | varchar | 注文キャンセルの理由。未キャンセルは null |
| クローズ済 | closed | boolean | 全項目完了で注文が閉じたか |
| テスト注文 | is_test | boolean | テスト注文か |
| 税込フラグ | taxes_included | boolean | 小計に税が含まれるか |
| 免税 | tax_exempt | boolean | 注文が免税か |
| 注文チャネル | source_name | varchar | 注文チャネル |
| 通貨コード | currency_code | varchar | 通貨 |
| PO番号 | po_number | varchar | 発注番号 (B2B) |
| 顧客ロケール | customer_locale | varchar | 購入時の言語地域 (例 en, fr-CA) |
| マーケ同意 | customer_accepts_marketing | boolean | 購入時のマーケメール受信同意 |
| 出荷件数 | fulfillments_count | integer | キャンセル含む出荷総数 |
| メールアドレス / 電話番号 / 備考 | email / phone / note | varchar | 連絡先・備考 |
| 配送先市区町村 / 配送先都道府県 / 配送先国 / 配送先国コード / 配送先郵便番号 | ship_city / ship_province / ship_country / ship_country_code / ship_zip | varchar | 配送先 |
| 請求先市区町村 / 請求先都道府県 / 請求先国 / 請求先国コード / 請求先郵便番号 | bill_city / bill_province / bill_country / bill_country_code / bill_zip | varchar | 請求先 |
| 請求=配送一致 | bill_matches_ship | boolean | 請求先と配送先が一致するか |
| 小計対象数量 | subtotal_line_items_quantity | integer | 小計に寄与する商品の合計数量 |
| 現小計対象数量 | current_subtotal_line_items_quantity | integer | 返品等後の小計対象数量 |
| 現重量 | current_total_weight | double | 返品後の合計重量 (g) |
| 合計金額 / 小計 / 税額 / 割引総額 / 送料 | total_price / subtotal_price / total_tax / total_discounts / total_shipping | double | 各金額 (作成時点) |
| 現在合計金額 | current_total_price | double | 返金反映後の現在合計 |
| 現小計金額 | current_subtotal_price | double | 返品後の小計 (税割引込) |
| 現税額合計 | current_total_tax | double | 返品後の税合計 |
| 現割引合計 | current_total_discounts | double | 返品後の割引合計 |
| 返金総額 | total_refunded | double | 返金総額 |
| 純支払額 | net_payment | double | 受領額 − 返金額 |
| 作成日時 / 更新日時 / 処理日時 / キャンセル日時 / クローズ日時 | created_at / updated_at / processed_at / cancelled_at / closed_at | timestamp | 各日時 |
| 注文dlt行ID | order_dlt_id | varchar | inline list 子 (discount_codes / tags / refunds / fulfillments / transactions) 結合用 dlt 行 ID |
