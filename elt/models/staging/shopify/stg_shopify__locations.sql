with source as (
    select * from {{ source('shopify_raw', 'locations') }}
)

select
    id                          as location_id,
    legacy_resource_id          as location_legacy_id,
    name                        as location_name,
    is_active,
    fulfills_online_orders,
    address__city               as city,
    address__province           as province,
    address__country            as country,
    address__country_code       as country_code,
    address__zip                as zip
from source
