{#
  ロケーションディメンション (在庫/フルフィルメント拠点)。1 行 = 1 拠点。
#}

select
    location_id,
    location_legacy_id,
    location_name,
    is_active,
    fulfills_online_orders,
    ships_inventory,
    has_active_inventory,
    address1,
    address2,
    city,
    province,
    province_code,
    country,
    country_code,
    zip,
    phone,
    latitude,
    longitude
from {{ ref('stg_shopify__locations') }}
