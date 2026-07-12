{#
  ロケーション×在庫アイテムの在庫数スナップショット。Bulk (locations → inventoryLevels)
  で全件取得。quantities (name/quantity のペア) は子テーブル inventory_levels__quantities
  へ正規化されるため、name ごとに横持ち集計する。
  location_id で stg_shopify__locations.location_id、inventory_item_id で
  stg_shopify__product_variants.inventory_item_id に紐づく。1 行 = (ロケーション × 在庫アイテム)。
#}
with levels as (
    select * from {{ source('shopify_raw', 'inventory_levels') }}
),

quantities as (
    select
        _dlt_parent_id,
        max(case when name = 'available' then cast(quantity as integer) end) as available,
        max(case when name = 'on_hand'   then cast(quantity as integer) end) as on_hand,
        max(case when name = 'committed' then cast(quantity as integer) end) as committed,
        max(case when name = 'incoming'  then cast(quantity as integer) end) as incoming
    from {{ source('shopify_raw', 'inventory_levels__quantities') }}
    group by 1
)

select
    l.id            as inventory_level_id,
    l.parent_id     as location_id,
    l.item__id      as inventory_item_id,
    l.item__sku     as sku,
    q.available,
    q.on_hand,
    q.committed,
    q.incoming
from levels l
left join quantities q on l._dlt_id = q._dlt_parent_id
