{#
  注文のフルフィルメント (出荷)。orders の inline list (fulfillments) が dlt により
  子テーブル orders__fulfillments へ正規化される。order_dlt_id で
  stg_shopify__orders.order_dlt_id に紐づく。1 行 = 1 出荷。
#}
with source as (
    select * from {{ source('shopify_raw', 'orders__fulfillments') }}
)

select
    id                                          as fulfillment_id,
    _dlt_parent_id                              as order_dlt_id,
    name                                        as fulfillment_name,
    status                                      as fulfillment_status,
    display_status,
    cast(total_quantity as integer)             as total_quantity,
    cast(created_at as timestamp)               as created_at,
    cast(updated_at as timestamp)               as updated_at,
    cast(estimated_delivery_at as timestamp)    as estimated_delivery_at,
    cast(in_transit_at as timestamp)            as in_transit_at,
    cast(delivered_at as timestamp)             as delivered_at

from source
