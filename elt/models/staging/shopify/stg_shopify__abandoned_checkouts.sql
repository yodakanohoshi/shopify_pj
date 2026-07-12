with source as (
    select * from {{ source('shopify_raw', 'abandoned_checkouts') }}
)

select
    id                                                      as checkout_id,
    customer__id                                            as customer_id,
    abandoned_checkout_url,
    note,
    taxes_included,
    cast(total_price_set__shop_money__amount as double)          as total_price,
    total_price_set__shop_money__currency_code                   as currency_code,
    cast(subtotal_price_set__shop_money__amount as double)       as subtotal_price,
    cast(total_line_items_price_set__shop_money__amount as double) as total_line_items_price,
    cast(total_tax_set__shop_money__amount as double)            as total_tax,
    cast(total_discount_set__shop_money__amount as double)       as total_discount,
    -- 地理 (配送先 / 請求先)
    shipping_address__city                                  as ship_city,
    shipping_address__country                               as ship_country,
    billing_address__city                                  as bill_city,
    billing_address__country                               as bill_country,
    cast(created_at as timestamp)                           as created_at,
    cast(updated_at as timestamp)                           as updated_at,
    cast(completed_at as timestamp)                         as completed_at,
    -- completed_at があれば後から購入に至った (復帰) とみなす
    (completed_at is not null)                              as is_recovered,
    -- inline list 子 (discount_codes) 結合用
    _dlt_id                                                 as checkout_dlt_id

from source
