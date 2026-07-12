{#
  注文の決済取引。orders の inline list (transactions) が dlt により子テーブル
  orders__transactions へ正規化される。order_dlt_id で stg_shopify__orders.order_dlt_id
  に紐づく。1 行 = 1 取引 (authorization / capture / refund / sale 等)。
#}
with source as (
    {{ raw_source(source('shopify_raw', 'orders__transactions'), [
        'id', '_dlt_parent_id', 'kind', 'status', 'gateway', 'test',
        'amount_set__shop_money__amount', 'amount_set__shop_money__currency_code',
        'created_at', 'processed_at'
    ]) }}
)

select
    {{ parse_gid_id('id') }}                        as transaction_id,
    _dlt_parent_id                                  as order_dlt_id,
    kind                                            as transaction_kind,
    status                                          as transaction_status,
    gateway,
    test                                            as is_test,
    cast(amount_set__shop_money__amount as double)  as amount,
    amount_set__shop_money__currency_code           as currency_code,
    cast(created_at as timestamp)                   as created_at,
    cast(processed_at as timestamp)                 as processed_at

from source
