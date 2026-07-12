with source as (
    {{ raw_source(source('shopify_raw', 'abandoned_checkout_line_items'), [
        'id',
        'parent_id',
        'product__id',
        'variant__id',
        'title',
        'quantity'
    ]) }}
)

select
    id                          as checkout_line_id,
    parent_id                   as checkout_id,
    product__id                 as product_id,
    variant__id                 as variant_id,
    title                       as product_title,
    cast(quantity as integer)   as quantity
from source
