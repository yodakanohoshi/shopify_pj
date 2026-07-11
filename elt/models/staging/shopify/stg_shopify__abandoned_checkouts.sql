with source as (
    select * from {{ source('shopify_raw', 'abandoned_checkouts') }}
)

select
    id                                                      as checkout_id,
    customer__id                                            as customer_id,
    abandoned_checkout_url,
    cast(total_price_set__shop_money__amount as double)     as total_price,
    total_price_set__shop_money__currency_code              as currency_code,
    cast(subtotal_price_set__shop_money__amount as double)  as subtotal_price,
    cast(created_at as timestamp)                           as created_at,
    cast(updated_at as timestamp)                           as updated_at,
    cast(completed_at as timestamp)                         as completed_at,
    -- completed_at があれば後から購入に至った (復帰) とみなす
    (completed_at is not null)                              as is_recovered

from source
