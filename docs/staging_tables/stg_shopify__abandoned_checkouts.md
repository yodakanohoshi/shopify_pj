# staging.stg_shopify__abandoned_checkouts

放棄チェックアウト。元: `raw.abandoned_checkouts`。粒度: 1 行 = 1 チェックアウト。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| カゴ落ちID | checkout_id | varchar | チェックアウト ID。**PK** |
| 顧客ID | customer_id | varchar | 顧客 ID (匿名は null) |
| カゴ落ちURL | abandoned_checkout_url | varchar | 復帰用 URL |
| メモ | note | varchar | 社内向けメモ |
| 税込フラグ | taxes_included | boolean | 価格に税を含むか |
| 合計金額 | total_price | double | 合計 |
| 通貨コード | currency_code | varchar | 通貨 |
| 小計 | subtotal_price | double | 小計 |
| 明細価格合計 | total_line_items_price | double | 全明細の価格合計 |
| 税額合計 | total_tax | double | チェックアウトの総税額 |
| 割引合計 | total_discount | double | 適用割引の総額 |
| 配送先市区町村 / 配送先国 | ship_city / ship_country | varchar | 配送先 |
| 請求先市区町村 / 請求先国 | bill_city / bill_country | varchar | 請求先 |
| 作成日時 / 更新日時 / 完了日時 | created_at / updated_at / completed_at | timestamp | 各日時 |
| 復帰済み | is_recovered | boolean | completed_at 非 null (後から購入=復帰) |
| カゴ落ちdlt行ID | checkout_dlt_id | varchar | inline list 子 (discount_codes) 結合用 dlt 行 ID |
