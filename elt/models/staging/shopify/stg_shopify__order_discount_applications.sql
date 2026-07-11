with source as (
    select * from {{ source('shopify_raw', 'orders__discount_applications') }}
)

select
    _dlt_id                                     as order_discount_id,
    _dlt_parent_id                              as order_dlt_id,
    code                                        as discount_code,
    title                                       as discount_title,
    allocation_method,
    target_selection,
    target_type,
    -- value は MoneyV2 か PricingPercentageValue のユニオン
    cast(value__amount as double)               as discount_amount,
    value__currency_code                        as discount_currency,
    cast(value__percentage as double)           as discount_percentage

from source
