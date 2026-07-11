{#
  注文ファクト。1 行 = 1 注文。売上/AOV/返金/チャネル/地理の分析基点。
#}

select
    order_id,
    order_name,
    customer_id,
    order_date,
    source_name,
    financial_status,
    fulfillment_status,
    is_cancelled,
    has_refund,
    currency_code,
    ship_country,
    ship_province,
    line_count,
    total_quantity,
    discount_code_count,
    first_discount_code,
    subtotal_price,
    total_discounts,
    total_tax,
    total_shipping,
    total_refunded,
    total_price,
    current_total_price,
    net_revenue,
    created_at,
    processed_at
from {{ ref('int_orders__enriched') }}
