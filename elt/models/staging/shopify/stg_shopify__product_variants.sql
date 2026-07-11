with source as (
    select * from {{ source('shopify_raw', 'product_variants') }}
)

select
    id                                                      as variant_id,
    legacy_resource_id                                      as variant_legacy_id,
    parent_id                                               as product_id,
    title                                                   as variant_title,
    sku,
    barcode,
    cast(price as double)                                   as price,
    cast(compare_at_price as double)                        as compare_at_price,
    -- 原価 (粗利計算に使用)
    cast(inventory_item__unit_cost__amount as double)       as unit_cost,
    inventory_item__unit_cost__currency_code                as unit_cost_currency,
    cast(inventory_item__measurement__weight__value as double) as weight_value,
    inventory_item__measurement__weight__unit               as weight_unit,
    cast(inventory_quantity as integer)                     as inventory_quantity,
    cast(position as integer)                               as position

from source
