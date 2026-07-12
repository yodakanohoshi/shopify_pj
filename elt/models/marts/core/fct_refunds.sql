{#
  返金ファクト。1 行 = 1 返金。注文粒度の total_refunded を裏付ける明細。
  返金額・返金日・注文/顧客の分析基点。
#}
with refunds as (
    select * from {{ ref('stg_shopify__order_refunds') }}
),

orders as (
    select order_id, order_dlt_id, customer_id from {{ ref('stg_shopify__orders') }}
)

select
    r.refund_id,
    o.order_id,
    o.customer_id,
    cast(r.created_at as date)  as refund_date,
    r.refund_amount,
    r.currency_code,
    r.note,
    r.created_at,
    r.processed_at
from refunds r
left join orders o on r.order_dlt_id = o.order_dlt_id
