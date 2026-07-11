{#
  注文明細ファクト。1 行 = 1 明細。商品別・カテゴリ別の売上分析に使う。
#}

with lines as (
    select * from {{ ref('int_order_lines__enriched') }}
)

select
    order_line_id,
    order_id,
    product_id,
    variant_id,
    product_title,
    product_type,
    vendor,
    sku,
    order_date,
    quantity,
    original_unit_price,
    discounted_unit_price,
    line_discount,
    net_line_revenue,
    currency_code
from lines
