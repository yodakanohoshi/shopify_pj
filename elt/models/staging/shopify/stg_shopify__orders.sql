with source as (
    select * from {{ source('shopify_raw', 'orders') }}
)

select
    -- 識別子
    id                                              as order_id,
    legacy_resource_id                              as order_legacy_id,
    name                                            as order_name,
    customer__id                                    as customer_id,

    -- ステータス
    display_financial_status                        as financial_status,
    display_fulfillment_status                      as fulfillment_status,
    currency_code,

    -- 連絡先
    email,
    phone,
    note,

    -- 金額 (GraphQL は文字列で返すため数値化)
    cast(total_price_set__shop_money__amount as double)        as total_price,
    cast(subtotal_price_set__shop_money__amount as double)     as subtotal_price,
    cast(total_tax_set__shop_money__amount as double)          as total_tax,
    cast(total_discounts_set__shop_money__amount as double)    as total_discounts,
    cast(total_shipping_price_set__shop_money__amount as double) as total_shipping,

    -- 日時
    cast(created_at as timestamp)                   as created_at,
    cast(updated_at as timestamp)                   as updated_at,
    cast(processed_at as timestamp)                 as processed_at,
    cast(cancelled_at as timestamp)                 as cancelled_at,
    cast(closed_at as timestamp)                    as closed_at,

    -- 子テーブル結合用のサロゲート (dlt の行 ID)
    _dlt_id                                         as order_dlt_id

from source
