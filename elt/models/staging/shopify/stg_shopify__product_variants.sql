with source as (
    select * from {{ source('shopify_raw', 'products__variants') }}
)

select
    id                                          as variant_id,
    legacy_resource_id                          as variant_legacy_id,
    _dlt_parent_id                              as product_dlt_id,
    title                                       as variant_title,
    sku,
    barcode,
    cast(price as double)                       as price,
    cast(compare_at_price as double)            as compare_at_price,
    cast(inventory_quantity as integer)         as inventory_quantity,
    cast(position as integer)                   as position,
    cast(created_at as timestamp)               as created_at,
    cast(updated_at as timestamp)               as updated_at

from source
