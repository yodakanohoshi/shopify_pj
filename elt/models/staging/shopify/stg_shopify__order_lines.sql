with source as (
    {{ raw_source(source('shopify_raw', 'order_line_items'), [
        'id', 'parent_id', 'product__id', 'variant__id', 'title', 'sku', 'vendor',
        'quantity', 'original_unit_price_set__shop_money__amount',
        'discounted_unit_price_set__shop_money__amount',
        'total_discount_set__shop_money__amount'
    ]) }}
)

select
    {{ parse_gid_id('id') }}                                      as order_line_id,
    {{ parse_gid_id('parent_id') }}                               as order_id,
    {{ parse_gid_id('product__id') }}                             as product_id,
    {{ parse_gid_id('variant__id') }}                             as variant_id,
    title                                                         as product_title,
    sku,
    vendor,
    cast(quantity as integer)                                     as quantity,
    cast(original_unit_price_set__shop_money__amount as double)   as original_unit_price,
    cast(discounted_unit_price_set__shop_money__amount as double) as discounted_unit_price,
    cast(total_discount_set__shop_money__amount as double)        as line_discount

from source
