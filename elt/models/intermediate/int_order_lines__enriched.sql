{#
  注文明細に注文日・商品属性・原価を結合し、粗利を算出する中間モデル。
  fct_order_lines / 商品別収益分析の素地。
#}

with lines as (
    select * from {{ ref('stg_shopify__order_lines') }}
),

orders as (
    select order_id, currency_code, created_at, financial_status
    from {{ ref('stg_shopify__orders') }}
),

products as (
    select product_id, product_title, product_type, vendor, category_name
    from {{ ref('stg_shopify__products') }}
),

variants as (
    select variant_id, unit_cost
    from {{ ref('stg_shopify__product_variants') }}
)

select
    l.order_line_id,
    o.order_id,
    l.product_id,
    l.variant_id,
    coalesce(p.product_title, l.product_title) as product_title,
    p.product_type,
    p.category_name,
    p.vendor,
    l.sku,
    l.quantity,
    l.original_unit_price,
    l.discounted_unit_price,
    l.line_discount,
    v.unit_cost,

    -- 純売上 (割引後単価 × 数量)
    l.discounted_unit_price * l.quantity            as net_line_revenue,
    -- 原価合計・粗利 (原価が取得できた明細のみ)
    v.unit_cost * l.quantity                        as line_cost,
    l.discounted_unit_price * l.quantity - v.unit_cost * l.quantity as gross_margin,

    o.currency_code,
    o.financial_status,
    cast(o.created_at as date)                      as order_date
from lines l
inner join orders o on l.order_id = o.order_id
left join products p on l.product_id = p.product_id
left join variants v on l.variant_id = v.variant_id
