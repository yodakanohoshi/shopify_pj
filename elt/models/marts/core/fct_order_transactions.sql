{#
  決済取引ファクト。1 行 = 1 取引 (authorization / capture / sale / refund / void)。
  決済ゲートウェイ別売上・入金・返金の分析基点。
#}
with transactions as (
    select * from {{ ref('stg_shopify__order_transactions') }}
),

orders as (
    select order_id, order_dlt_id, customer_id from {{ ref('stg_shopify__orders') }}
)

select
    t.transaction_id,
    o.order_id,
    o.customer_id,
    t.transaction_kind,
    t.transaction_status,
    t.gateway,
    t.is_test,
    t.amount,
    t.currency_code,
    cast(t.processed_at as date) as transaction_date,
    t.created_at,
    t.processed_at
from transactions t
left join orders o on t.order_dlt_id = o.order_dlt_id
