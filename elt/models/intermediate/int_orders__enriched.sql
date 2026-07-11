{#
  注文ヘッダに明細集計・顧客属性・返金反映後の純売上を結合した中間モデル。
  fct_orders の素地。
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

codes as (
    select order_dlt_id, count(*) as discount_code_count, min(discount_code) as first_discount_code
    from {{ ref('stg_shopify__order_discount_codes') }}
    group by 1
),

line_agg as (
    select
        order_id,
        count(*)            as line_count,
        sum(quantity)       as total_quantity,
        sum(line_discount)  as line_discount_total
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
    o.source_name,
    o.currency_code,
    o.ship_country,
    o.ship_province,
    o.ship_city,

    -- 金額
    o.total_price,
    o.subtotal_price,
    o.total_tax,
    o.total_discounts,
    o.total_shipping,
    o.total_refunded,
    o.current_total_price,
    -- 純売上: 小計 − 割引 − 返金
    o.subtotal_price - o.total_discounts - o.total_refunded as net_revenue,

    -- 割引
    coalesce(cd.discount_code_count, 0)  as discount_code_count,
    cd.first_discount_code,

    -- 明細集計
    coalesce(la.line_count, 0)          as line_count,
    coalesce(la.total_quantity, 0)      as total_quantity,
    coalesce(la.line_discount_total, 0) as line_discount_total,

    -- 日時・フラグ
    o.created_at,
    o.processed_at,
    o.cancelled_at,
    cast(o.created_at as date)          as order_date,
    (o.cancelled_at is not null)        as is_cancelled,
    (o.total_refunded > 0)              as has_refund

from orders o
left join line_agg la on o.order_id = la.order_id
left join customers c on o.customer_id = c.customer_id
left join codes cd on o.order_dlt_id = cd.order_dlt_id
