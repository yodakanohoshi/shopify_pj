{#
  顧客に実注文からの集計指標と住所数を結合した中間モデル。
  dim_customers の素地。
#}

with customers as (
    select * from {{ ref('stg_shopify__customers') }}
),

order_stats as (
    select
        customer_id,
        count(*)            as orders_count,
        sum(net_revenue)    as revenue_total,
        avg(net_revenue)    as avg_order_value,
        min(order_date)     as first_order_date,
        max(order_date)     as latest_order_date
    from {{ ref('int_orders__enriched') }}
    where customer_id is not null
      and not is_cancelled
    group by 1
),

address_agg as (
    select customer_id, count(*) as address_count
    from {{ ref('stg_shopify__customer_addresses') }}
    group by 1
)

select
    c.customer_id,
    c.customer_legacy_id,
    c.first_name,
    c.last_name,
    c.email,
    c.email_marketing_state,
    c.email_marketing_opt_in_level,
    -- 配信可能フラグ
    (c.email_marketing_state = 'SUBSCRIBED')    as is_email_subscribed,
    c.customer_state,
    c.tax_exempt,
    c.customer_locale,
    c.lifetime_duration,
    c.country,
    c.country_code,
    c.city,
    c.lifetime_amount_spent,
    coalesce(os.orders_count, 0)        as orders_count,
    coalesce(os.revenue_total, 0)       as revenue_total,
    os.avg_order_value,
    os.first_order_date,
    os.latest_order_date,
    coalesce(aa.address_count, 0)       as address_count,
    -- 簡易セグメント
    case
        when coalesce(os.orders_count, 0) = 0 then 'prospect'
        when os.orders_count = 1              then 'one_time'
        when os.orders_count between 2 and 4  then 'repeat'
        else 'loyal'
    end                                 as customer_segment,
    c.created_at,
    c.updated_at
from customers c
left join order_stats os on c.customer_id = os.customer_id
left join address_agg aa on c.customer_id = aa.customer_id
