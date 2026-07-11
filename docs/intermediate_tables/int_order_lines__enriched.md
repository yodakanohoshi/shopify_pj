# intermediate.int_order_lines__enriched

注文明細 + 商品属性 + 原価/粗利。粒度: 1 行 = 1 明細。

| カラム | 型 | 説明 |
|---|---|---|
| order_line_id | varchar | 明細 ID。**PK** |
| order_id | varchar | 注文 ID (FK) |
| product_id / variant_id | varchar | 商品 / バリアント ID |
| product_title / product_type / category_name / vendor | varchar | 商品属性 (結合) |
| sku | varchar | SKU |
| quantity | integer | 数量 |
| original_unit_price / discounted_unit_price / line_discount | double | 単価・割引 |
| unit_cost | double | 原価単価 (バリアントより) |
| net_line_revenue | double | 純売上 = 割引後単価 × 数量 |
| line_cost | double | 原価合計 = 原価単価 × 数量 |
| gross_margin | double | 粗利 = 純売上 − 原価合計 |
| currency_code / financial_status | varchar | 通貨 / 支払ステータス |
| order_date | date | 注文日 |
