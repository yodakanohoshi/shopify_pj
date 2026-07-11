{#
  割引に、コード別利用回数の集計と注文適用実績を結合した中間モデル。
  fct_discount_performance の素地。
#}

with discounts as (
    select * from {{ ref('stg_shopify__discounts') }}
),

codes as (
    select
        discount_dlt_id,
        count(*)                as code_count,
        sum(code_usage_count)   as code_usage_total,
        min(discount_code)      as sample_code
    from {{ ref('stg_shopify__discount_codes') }}
    group by 1
),

-- 注文側で実際に使われた割引コードの実績 (コード文字列で突合)
applied as (
    select
        discount_code,
        count(distinct order_dlt_id)    as orders_with_code,
        sum(discount_amount)            as applied_amount_total
    from {{ ref('stg_shopify__order_discount_applications') }}
    where discount_code is not null
    group by 1
)

select
    d.discount_id,
    d.discount_type,
    d.discount_method,
    d.discount_title,
    d.discount_status,
    d.discount_percentage,
    d.discount_amount,
    d.discount_currency,
    d.usage_limit,
    d.total_usage_count,
    coalesce(c.code_count, 0)           as code_count,
    coalesce(c.code_usage_total, 0)     as code_usage_total,
    c.sample_code,
    coalesce(a.orders_with_code, 0)     as orders_with_code,
    coalesce(a.applied_amount_total, 0) as applied_amount_total,
    d.starts_at,
    d.ends_at
from discounts d
left join codes c on d.discount_dlt_id = c.discount_dlt_id
left join applied a on c.sample_code = a.discount_code
