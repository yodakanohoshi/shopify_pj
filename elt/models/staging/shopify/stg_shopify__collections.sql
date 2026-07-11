with source as (
    select * from {{ source('shopify_raw', 'collections') }}
)

select
    id                              as collection_id,
    title                           as collection_title,
    handle,
    sort_order,
    cast(products_count__count as integer) as products_count,
    cast(updated_at as timestamp)   as updated_at
from source
