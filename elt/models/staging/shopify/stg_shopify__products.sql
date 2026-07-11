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
    -- 標準タクソノミのカテゴリ
    category__id                                as category_id,
    category__name                              as category_name,
    category__full_name                         as category_full_name,
    cast(total_inventory as integer)            as total_inventory,
    cast(created_at as timestamp)               as created_at,
    cast(updated_at as timestamp)               as updated_at,
    cast(published_at as timestamp)             as published_at

from source
