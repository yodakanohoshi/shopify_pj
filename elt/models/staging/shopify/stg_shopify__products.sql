with source as (
    select * from {{ source('shopify_raw', 'products') }}
)

select
    id                                          as product_id,
    legacy_resource_id                          as product_legacy_id,
    title                                       as product_title,
    handle,
    product_type,
    vendor,
    status                                      as product_status,
    cast(total_inventory as integer)            as total_inventory,
    cast(created_at as timestamp)               as created_at,
    cast(updated_at as timestamp)               as updated_at,
    cast(published_at as timestamp)             as published_at,
    _dlt_id                                     as product_dlt_id

from source
