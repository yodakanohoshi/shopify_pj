with source as (
    select * from {{ source('shopify_raw', 'customers') }}
)

select
    id                                          as customer_id,
    legacy_resource_id                          as customer_legacy_id,
    first_name,
    last_name,
    email,
    phone,
    state                                       as customer_state,
    verified_email,
    cast(number_of_orders as integer)           as number_of_orders,
    cast(amount_spent__amount as double)        as lifetime_amount_spent,
    amount_spent__currency_code                 as amount_spent_currency,
    default_address__city                       as city,
    default_address__province                   as province,
    default_address__country                    as country,
    default_address__country_code_v2            as country_code,
    default_address__zip                        as zip,
    cast(created_at as timestamp)               as created_at,
    cast(updated_at as timestamp)               as updated_at

from source
