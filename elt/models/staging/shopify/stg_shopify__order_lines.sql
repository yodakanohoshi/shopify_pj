with source as (
    select * from {{ source('shopify_raw', 'orders__line_items') }}
)

select
    _dlt_id                                                     as order_line_id,
    _dlt_parent_id                                              as order_dlt_id,
    id                                                          as line_item_gid,
    product__id                                                as product_id,
    variant__id                                                as variant_id,
    title                                                       as product_title,
    sku,
    vendor,
    cast(quantity as integer)                                  as quantity,
    cast(original_unit_price_set__shop_money__amount as double)   as original_unit_price,
    cast(discounted_unit_price_set__shop_money__amount as double) as discounted_unit_price,
    cast(total_discount_set__shop_money__amount as double)        as line_discount

from source
