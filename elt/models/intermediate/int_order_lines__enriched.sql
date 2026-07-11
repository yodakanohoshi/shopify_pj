{#
  注文明細に注文日・商品情報を結合した中間モデル。
  fct_order_lines / 商品別売上分析の素地。
#}

with lines as (
    select * from {{ ref('stg_shopify__order_lines') }}
),

orders as (
    select order_id, order_dlt_id, currency_code, created_at, financial_status
    from {{ ref('stg_shopify__orders') }}
),

products as (
    select product_id, product_title, product_type, vendor
    from {{ ref('stg_shopify__products') }}
)

select
    l.order_line_id,
    o.order_id,
    l.product_id,
    l.variant_id,
    coalesce(p.product_title, l.product_title) as product_title,
    p.product_type,
    p.vendor,
    l.sku,
    l.quantity,
    l.original_unit_price,
    l.discounted_unit_price,
    l.line_discount,
    -- 明細の純売上 (割引後単価 × 数量)
    l.discounted_unit_price * l.quantity        as net_line_revenue,
    o.currency_code,
    o.financial_status,
    cast(o.created_at as date)                  as order_date
from lines l
inner join orders o on l.order_dlt_id = o.order_dlt_id
left join products p on l.product_id = p.product_id
