{#
  在庫レベルファクト。1 行 = (ロケーション × 在庫アイテム) の在庫スナップショット。
  在庫アイテムをバリアント/商品に、ロケーションを拠点に紐づける。欠品・在庫回転の分析基点。
#}
with levels as (
    select * from {{ ref('stg_shopify__inventory_levels') }}
),

locations as (
    select location_id, location_name from {{ ref('stg_shopify__locations') }}
),

variants as (
    select variant_id, product_id, inventory_item_id from {{ ref('stg_shopify__product_variants') }}
)

select
    l.inventory_level_id,
    l.location_id,
    loc.location_name,
    l.inventory_item_id,
    v.variant_id,
    v.product_id,
    l.sku,
    l.available,
    l.on_hand,
    l.committed,
    l.incoming
from levels l
left join locations loc on l.location_id = loc.location_id
left join variants v on l.inventory_item_id = v.inventory_item_id
