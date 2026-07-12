with source as (
    select * from {{ source('shopify_raw', 'products') }}
)

select
    id                                          as product_id,
    legacy_resource_id                          as product_legacy_id,
    title                                       as product_title,
    handle,
    description                                  as product_description,
    product_type,
    vendor,
    status                                      as product_status,
    template_suffix,
    online_store_url,
    is_gift_card,
    tracks_inventory,
    has_only_default_variant,
    requires_selling_plan,
    -- 標準タクソノミのカテゴリ
    category__id                                as category_id,
    category__name                              as category_name,
    category__full_name                         as category_full_name,
    -- SEO
    seo__title                                  as seo_title,
    seo__description                            as seo_description,
    cast(variants_count__count as integer)      as variants_count,
    cast(total_inventory as integer)            as total_inventory,
    cast(created_at as timestamp)               as created_at,
    cast(updated_at as timestamp)               as updated_at,
    cast(published_at as timestamp)             as published_at

from source
