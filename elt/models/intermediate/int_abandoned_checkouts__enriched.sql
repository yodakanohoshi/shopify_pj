{#
  放棄チェックアウトに明細集計を結合した中間モデル。
  fct_abandoned_checkouts の素地。
#}

with checkouts as (
    select * from {{ ref('stg_shopify__abandoned_checkouts') }}
),

line_agg as (
    select
        checkout_id,
        count(*)        as line_count,
        sum(quantity)   as total_quantity
    from {{ ref('stg_shopify__abandoned_checkout_lines') }}
    group by 1
)

select
    ck.checkout_id,
    ck.customer_id,
    ck.currency_code,
    ck.total_price,
    ck.subtotal_price,
    coalesce(la.line_count, 0)      as line_count,
    coalesce(la.total_quantity, 0)  as total_quantity,
    ck.is_recovered,
    ck.created_at,
    ck.completed_at,
    cast(ck.created_at as date)     as checkout_date
from checkouts ck
left join line_agg la on ck.checkout_id = la.checkout_id
