{#
  顧客ディメンション。属性 + 実注文集計 + 配信同意 + セグメント。1 行 = 1 顧客。
#}

select
    customer_id,
    customer_legacy_id,
    first_name,
    last_name,
    email,
    is_email_subscribed,
    email_marketing_state,
    customer_state,
    customer_segment,
    country,
    country_code,
    city,
    lifetime_amount_spent,
    orders_count,
    revenue_total,
    avg_order_value,
    address_count,
    first_order_date,
    latest_order_date,
    created_at,
    updated_at
from {{ ref('int_customers__enriched') }}
