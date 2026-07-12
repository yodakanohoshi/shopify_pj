with source as (
    select * from {{ source('shopify_raw', 'orders') }}
)

select
    -- 識別子
    id                                              as order_id,
    legacy_resource_id                              as order_legacy_id,
    name                                            as order_name,
    cast(number as integer)                         as order_number,
    confirmation_number,
    customer__id                                    as customer_id,

    -- ステータス・チャネル
    display_financial_status                        as financial_status,
    display_fulfillment_status                      as fulfillment_status,
    cancel_reason,
    closed,
    test                                            as is_test,
    taxes_included,
    tax_exempt,
    currency_code,
    source_name,
    po_number,
    customer_locale,
    customer_accepts_marketing,
    cast(fulfillments_count__count as integer)      as fulfillments_count,

    -- 連絡先
    email,
    phone,
    note,

    -- 地理 (配送先)
    shipping_address__city                          as ship_city,
    shipping_address__province                      as ship_province,
    shipping_address__country                       as ship_country,
    shipping_address__country_code_v2               as ship_country_code,
    shipping_address__zip                           as ship_zip,
    -- 地理 (請求先)
    billing_address__city                           as bill_city,
    billing_address__province                       as bill_province,
    billing_address__country                        as bill_country,
    billing_address__country_code_v2                as bill_country_code,
    billing_address__zip                            as bill_zip,
    billing_address_matches_shipping_address        as bill_matches_ship,

    -- 数量
    cast(subtotal_line_items_quantity as integer)          as subtotal_line_items_quantity,
    cast(current_subtotal_line_items_quantity as integer)  as current_subtotal_line_items_quantity,
    cast(current_total_weight as double)                   as current_total_weight,

    -- 金額 (作成時点)
    cast(total_price_set__shop_money__amount as double)          as total_price,
    cast(subtotal_price_set__shop_money__amount as double)       as subtotal_price,
    cast(total_tax_set__shop_money__amount as double)            as total_tax,
    cast(total_discounts_set__shop_money__amount as double)      as total_discounts,
    cast(total_shipping_price_set__shop_money__amount as double) as total_shipping,
    -- 返金反映後の現在値
    cast(current_total_price_set__shop_money__amount as double)     as current_total_price,
    cast(current_subtotal_price_set__shop_money__amount as double)  as current_subtotal_price,
    cast(current_total_tax_set__shop_money__amount as double)       as current_total_tax,
    cast(current_total_discounts_set__shop_money__amount as double) as current_total_discounts,
    cast(total_refunded_set__shop_money__amount as double)          as total_refunded,
    cast(net_payment_set__shop_money__amount as double)             as net_payment,

    -- 日時
    cast(created_at as timestamp)                   as created_at,
    cast(updated_at as timestamp)                   as updated_at,
    cast(processed_at as timestamp)                 as processed_at,
    cast(cancelled_at as timestamp)                 as cancelled_at,
    cast(closed_at as timestamp)                    as closed_at,

    -- inline list 子テーブル (discount_codes / tags / refunds / fulfillments / transactions) 結合用
    _dlt_id                                         as order_dlt_id

from source
