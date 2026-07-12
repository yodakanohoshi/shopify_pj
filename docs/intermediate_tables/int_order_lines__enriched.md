# intermediate.int_order_lines__enriched

注文明細 + 商品属性 + 原価/粗利。粒度: 1 行 = 1 明細。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 明細ID | order_line_id | varchar | 明細 ID。**PK** |
| 注文ID | order_id | varchar | 注文 ID (FK) |
| 商品ID / バリアントID | product_id / variant_id | varchar | 商品 / バリアント ID |
| 商品名 / 商品タイプ / カテゴリ名 / ベンダー | product_title / product_type / category_name / vendor | varchar | 商品属性 (結合) |
| SKU | sku | varchar | SKU |
| 数量 | quantity | integer | 数量 |
| 単価(定価) / 割引後単価 / 明細割引額 | original_unit_price / discounted_unit_price / line_discount | double | 単価・割引 |
| 原価 | unit_cost | double | 原価単価 (バリアントより) |
| 明細純売上 | net_line_revenue | double | 純売上 = 割引後単価 × 数量 |
| 明細原価 | line_cost | double | 原価合計 = 原価単価 × 数量 |
| 粗利 | gross_margin | double | 粗利 = 純売上 − 原価合計 |
| 通貨コード / 支払ステータス | currency_code / financial_status | varchar | 通貨 / 支払ステータス |
| 注文日 | order_date | date | 注文日 |
