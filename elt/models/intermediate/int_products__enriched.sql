{#
  商品にバリアント集計 (価格レンジ・平均原価・在庫) を結合した中間モデル。
  dim_products の素地。
#}

with products as (
    select * from {{ ref('stg_shopify__products') }}
),

variant_agg as (
    select
        product_id,
        count(*)                as variant_count,
        min(price)              as min_price,
        max(price)              as max_price,
        avg(unit_cost)          as avg_unit_cost,
        sum(inventory_quantity) as total_inventory_qty
    from {{ ref('stg_shopify__product_variants') }}
    group by 1
)

select
    p.product_id,
    p.product_legacy_id,
    p.product_title,
    p.handle,
    p.product_type,
    p.category_name,
    p.category_full_name,
    p.vendor,
    p.product_status,
    p.product_description,
    p.is_gift_card,
    p.tracks_inventory,
    p.has_only_default_variant,
    p.variants_count               as variants_count_reported,
    coalesce(va.variant_count, 0)   as variant_count,
    va.min_price,
    va.max_price,
    va.avg_unit_cost,
    -- 粗利率 (最低価格ベースの概算)
    case when va.min_price > 0 and va.avg_unit_cost is not null
        then round((va.min_price - va.avg_unit_cost) / va.min_price, 4)
    end                             as est_margin_rate,
    coalesce(va.total_inventory_qty, p.total_inventory) as total_inventory,
    p.created_at,
    p.published_at
from products p
left join variant_agg va on p.product_id = va.product_id
