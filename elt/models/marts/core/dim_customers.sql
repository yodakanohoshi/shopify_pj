{#
  顧客ディメンション。API 由来の生涯指標に加え、実注文からの集計を付与する。
#}

with customers as (
    select * from {{ ref('stg_shopify__customers') }}
),

order_stats as (
    select
        customer_id,
        count(*)                        as orders_count,
        sum(total_price)                as revenue_total,
        min(order_date)                 as first_order_date,
        max(order_date)                 as latest_order_date
    from {{ ref('int_orders__enriched') }}
    where customer_id is not null
      and not is_cancelled
    group by 1
)

select
    c.customer_id,
    c.customer_legacy_id,
    c.first_name,
    c.last_name,
    c.email,
    c.customer_state,
    c.country,
    c.country_code,
    c.city,
    c.lifetime_amount_spent,
    coalesce(os.orders_count, 0)        as orders_count,
    coalesce(os.revenue_total, 0)       as revenue_total,
    os.first_order_date,
    os.latest_order_date,
    c.created_at,
    c.updated_at
from customers c
left join order_stats os on c.customer_id = os.customer_id
