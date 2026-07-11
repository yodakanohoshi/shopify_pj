{#
  注文ヘッダに明細集計と顧客情報を結合した中間モデル。
  fct_orders の素地となる。
#}

with orders as (
    select * from {{ ref('stg_shopify__orders') }}
),

lines as (
    select * from {{ ref('stg_shopify__order_lines') }}
),

customers as (
    select * from {{ ref('stg_shopify__customers') }}
),

line_agg as (
    select
        order_dlt_id,
        count(*)                    as line_count,
        sum(quantity)               as total_quantity,
        sum(line_discount)          as line_discount_total
    from lines
    group by 1
)

select
    o.order_id,
    o.order_name,
    o.order_legacy_id,
    o.customer_id,
    c.email                         as customer_email,
    c.country                       as customer_country,
    o.financial_status,
    o.fulfillment_status,
    o.currency_code,
    o.total_price,
    o.subtotal_price,
    o.total_tax,
    o.total_discounts,
    o.total_shipping,
    coalesce(la.line_count, 0)      as line_count,
    coalesce(la.total_quantity, 0)  as total_quantity,
    coalesce(la.line_discount_total, 0) as line_discount_total,
    o.created_at,
    o.processed_at,
    o.cancelled_at,
    cast(o.created_at as date)      as order_date,
    (o.cancelled_at is not null)    as is_cancelled
from orders o
left join line_agg la on o.order_dlt_id = la.order_dlt_id
left join customers c on o.customer_id = c.customer_id
