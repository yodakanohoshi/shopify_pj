with source as (
    select * from {{ source('shopify_raw', 'discounts') }}
)

select
    id                                          as discount_id,
    discount_type,
    case
        when discount_type like 'DiscountCode%'      then 'code'
        when discount_type like 'DiscountAutomatic%' then 'automatic'
        else 'other'
    end                                         as discount_method,
    title                                       as discount_title,
    status                                      as discount_status,
    summary,
    cast(usage_limit as integer)                as usage_limit,
    applies_once_per_customer,
    cast(async_usage_count as integer)          as total_usage_count,
    cast(customer_gets__value__percentage as double)     as discount_percentage,
    cast(customer_gets__value__amount__amount as double) as discount_amount,
    customer_gets__value__amount__currency_code          as discount_currency,
    cast(starts_at as timestamp)                as starts_at,
    cast(ends_at as timestamp)                  as ends_at,
    _dlt_id                                     as discount_dlt_id

from source
