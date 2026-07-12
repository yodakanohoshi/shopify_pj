with source as (
    {{ raw_source(source('shopify_raw', 'customer_addresses'), [
        'id', 'parent_id', 'city', 'province', 'country',
        'country_code_v2', 'zip'
    ]) }}
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
