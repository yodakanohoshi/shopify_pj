with source as (
    select * from {{ source('shopify_raw', 'locations') }}
)

select
    id                          as location_id,
    legacy_resource_id          as location_legacy_id,
    name                        as location_name,
    is_active,
    fulfills_online_orders,
    ships_inventory,
    has_active_inventory,
    address__address1           as address1,
    address__address2           as address2,
    address__city               as city,
    address__province           as province,
    address__province_code      as province_code,
    address__country            as country,
    address__country_code       as country_code,
    address__zip                as zip,
    address__phone              as phone,
    cast(address__latitude as double)  as latitude,
    cast(address__longitude as double) as longitude
from source
