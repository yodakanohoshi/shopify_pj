{#
  注文明細ファクト。1 行 = 1 明細。商品/カテゴリ別の売上・粗利分析。
#}

select
    order_line_id,
    order_id,
    product_id,
    variant_id,
    product_title,
    product_type,
    category_name,
    vendor,
    sku,
    order_date,
    quantity,
    original_unit_price,
    discounted_unit_price,
    line_discount,
    unit_cost,
    net_line_revenue,
    line_cost,
    gross_margin,
    currency_code
from {{ ref('int_order_lines__enriched') }}
