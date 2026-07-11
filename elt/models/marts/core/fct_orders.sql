{#
  注文ファクト。1 行 = 1 注文。BI の売上/AOV 分析の基点。
#}

with orders as (
    select * from {{ ref('int_orders__enriched') }}
)

select
    order_id,
    order_name,
    customer_id,
    order_date,
    financial_status,
    fulfillment_status,
    is_cancelled,
    currency_code,
    line_count,
    total_quantity,
    subtotal_price,
    total_discounts,
    total_tax,
    total_shipping,
    total_price,
    -- 純売上 (割引後・税送料除く近似)
    subtotal_price - total_discounts    as net_revenue,
    created_at,
    processed_at
from orders
