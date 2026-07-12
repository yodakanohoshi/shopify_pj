# marts.fct_order_lines

注文明細ファクト。商品/カテゴリ別の売上・粗利分析。粒度: 1 行 = 1 明細。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 明細ID | order_line_id | varchar | 数値ID (gid から抽出)。**PK** |
| 注文ID | order_id | varchar | 数値ID (gid から抽出)。**FK → fct_orders** |
| 商品ID / バリアントID | product_id / variant_id | varchar | 数値ID (gid から抽出) |
| 商品名 / 商品タイプ / カテゴリ名 / ベンダー | product_title / product_type / category_name / vendor | varchar | 商品属性 |
| SKU | sku | varchar | SKU |
| 注文日 | order_date | date | 注文日 |
| 数量 | quantity | integer | 数量 |
| 単価(定価) / 割引後単価 / 明細割引額 | original_unit_price / discounted_unit_price / line_discount | double | 単価・割引 |
| 原価単価 / 原価合計 | unit_cost / line_cost | double | 原価単価 / 原価合計 |
| 純売上 | net_line_revenue | double | 純売上 = 割引後単価 × 数量 |
| 粗利 | gross_margin | double | 粗利 = 純売上 − 原価合計 |
| 通貨コード | currency_code | varchar | 通貨 |
