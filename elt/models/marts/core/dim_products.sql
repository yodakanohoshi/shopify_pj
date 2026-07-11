{#
  商品ディメンション。バリアントの価格レンジと在庫を集約する。
#}

with products as (
    select * from {{ ref('stg_shopify__products') }}
),

variant_agg as (
    select
        product_dlt_id,
        count(*)                    as variant_count,
        min(price)                  as min_price,
        max(price)                  as max_price,
        sum(inventory_quantity)     as total_inventory_qty
    from {{ ref('stg_shopify__product_variants') }}
    group by 1
)

select
    p.product_id,
    p.product_legacy_id,
    p.product_title,
    p.handle,
    p.product_type,
    p.vendor,
    p.product_status,
    coalesce(va.variant_count, 0)   as variant_count,
    va.min_price,
    va.max_price,
    coalesce(va.total_inventory_qty, p.total_inventory) as total_inventory,
    p.created_at,
    p.published_at
from products p
left join variant_agg va on p.product_dlt_id = va.product_dlt_id
