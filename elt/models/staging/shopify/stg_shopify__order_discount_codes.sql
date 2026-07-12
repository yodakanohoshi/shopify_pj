{#
  注文に適用された割引コード文字列。orders の inline list (discountCodes) が
  dlt により子テーブル orders__discount_codes (value 列) へ正規化される。
  order_dlt_id で stg_shopify__orders.order_dlt_id に紐づく。
#}
with source as (
    {{ raw_source(source('shopify_raw', 'orders__discount_codes'), [
        '_dlt_parent_id', 'value'
    ]) }}
)

select
    _dlt_parent_id      as order_dlt_id,
    value               as discount_code
from source
