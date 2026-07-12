{#
  フルフィルメント (出荷) ファクト。1 行 = 1 出荷。
  配送リードタイム・出荷状況の分析基点。
#}
with fulfillments as (
    select * from {{ ref('stg_shopify__fulfillments') }}
),

orders as (
    select order_id, order_dlt_id, customer_id, created_at as order_created_at
    from {{ ref('stg_shopify__orders') }}
)

select
    f.fulfillment_id,
    o.order_id,
    o.customer_id,
    f.fulfillment_name,
    f.fulfillment_status,
    f.display_status,
    f.total_quantity,
    cast(f.created_at as date)  as fulfilled_date,
    f.created_at,
    f.updated_at,
    f.estimated_delivery_at,
    f.in_transit_at,
    f.delivered_at,
    -- 受注から出荷までの日数
    date_diff('day', o.order_created_at, f.created_at) as days_to_fulfill
from fulfillments f
left join orders o on f.order_dlt_id = o.order_dlt_id
