{#
  商品ディメンション。価格レンジ・平均原価・粗利率・カテゴリ・在庫。1 行 = 1 商品。
#}

select
    product_id,
    product_legacy_id,
    product_title,
    handle,
    product_type,
    category_name,
    category_full_name,
    vendor,
    product_status,
    tags,
    sku_list,
    jan_list,
    is_gift_card,
    tracks_inventory,
    has_only_default_variant,
    variants_count_reported,
    variant_count,
    min_price,
    max_price,
    avg_unit_cost,
    est_margin_rate,
    total_inventory,
    created_at,
    published_at
from {{ ref('int_products__enriched') }}
