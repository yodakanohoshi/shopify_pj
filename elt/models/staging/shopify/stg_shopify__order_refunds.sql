{#
  注文の返金。orders の inline list (refunds) が dlt により子テーブル
  orders__refunds へ正規化される。order_dlt_id で stg_shopify__orders.order_dlt_id に紐づく。
  1 行 = 1 返金。
#}
with source as (
    {{ raw_source(source('shopify_raw', 'orders__refunds'), [
        'id', '_dlt_parent_id', 'note',
        'total_refunded_set__shop_money__amount',
        'total_refunded_set__shop_money__currency_code',
        'created_at', 'processed_at'
    ]) }}
)

select
    id                                                      as refund_id,
    _dlt_parent_id                                          as order_dlt_id,
    note,
    cast(total_refunded_set__shop_money__amount as double)  as refund_amount,
    total_refunded_set__shop_money__currency_code           as currency_code,
    cast(created_at as timestamp)                           as created_at,
    cast(processed_at as timestamp)                         as processed_at

from source
