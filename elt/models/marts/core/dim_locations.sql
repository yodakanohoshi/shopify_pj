{#
  ロケーションディメンション (在庫/フルフィルメント拠点)。1 行 = 1 拠点。
#}

select
    location_id,
    location_legacy_id,
    location_name,
    is_active,
    fulfills_online_orders,
    city,
    province,
    country,
    country_code,
    zip
from {{ ref('stg_shopify__locations') }}
