with source as (
    select * from {{ source('shopify_raw', 'collections') }}
)

select
    id                              as collection_id,
    title                           as collection_title,
    handle,
    description                     as collection_description,
    template_suffix,
    sort_order,
    seo__title                      as seo_title,
    seo__description                as seo_description,
    cast(products_count__count as integer) as products_count,
    cast(updated_at as timestamp)   as updated_at
from source
