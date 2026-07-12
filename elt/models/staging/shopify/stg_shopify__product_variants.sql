with source as (
    {{ raw_source(source('shopify_raw', 'product_variants'), [
        'id', 'legacy_resource_id', 'parent_id', 'title', 'display_name',
        'sku', 'barcode', 'price', 'compare_at_price', 'available_for_sale',
        'taxable', 'inventory_policy',
        'inventory_item__id', 'inventory_item__tracked', 'inventory_item__requires_shipping',
        'inventory_item__unit_cost__amount', 'inventory_item__unit_cost__currency_code',
        'inventory_item__measurement__weight__value', 'inventory_item__measurement__weight__unit',
        'inventory_quantity', 'sellable_online_quantity', 'position',
        'created_at', 'updated_at'
    ]) }}
)

select
    id                                                      as variant_id,
    legacy_resource_id                                      as variant_legacy_id,
    parent_id                                               as product_id,
    title                                                   as variant_title,
    display_name                                            as variant_display_name,
    sku,
    barcode,
    cast(price as double)                                   as price,
    cast(compare_at_price as double)                        as compare_at_price,
    available_for_sale,
    taxable,
    inventory_policy,
    -- 在庫アイテム (在庫レベルとの結合キー)
    inventory_item__id                                      as inventory_item_id,
    inventory_item__tracked                                 as inventory_tracked,
    inventory_item__requires_shipping                       as requires_shipping,
    -- 原価 (粗利計算に使用)
    cast(inventory_item__unit_cost__amount as double)       as unit_cost,
    inventory_item__unit_cost__currency_code                as unit_cost_currency,
    cast(inventory_item__measurement__weight__value as double) as weight_value,
    inventory_item__measurement__weight__unit               as weight_unit,
    cast(inventory_quantity as integer)                     as inventory_quantity,
    cast(sellable_online_quantity as integer)               as sellable_online_quantity,
    cast(position as integer)                               as position,
    cast(created_at as timestamp)                           as created_at,
    cast(updated_at as timestamp)                           as updated_at

from source
