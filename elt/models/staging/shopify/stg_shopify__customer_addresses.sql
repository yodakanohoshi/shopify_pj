with source as (
    select * from {{ source('shopify_raw', 'customer_addresses') }}
)

select
    id                          as address_id,
    parent_id                   as customer_id,
    city,
    province,
    country,
    country_code_v2             as country_code,
    zip
from source
