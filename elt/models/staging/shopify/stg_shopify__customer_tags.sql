{#
  顧客タグ (long 形式)。1 行 = (顧客 × タグ)。

  Shopify の customer.tags は [String!]! (scalar のリスト)。dlt はこれを
  子テーブル customers__tags (値は value 列) へ正規化する。親への参照は
  gid ではなく dlt 内部行 ID (_dlt_parent_id → customers._dlt_id) なので、
  raw customers と結合して顧客 gid を取り出し、数値 ID へ変換する。
#}
with tags as (
    {{ raw_source(source('shopify_raw', 'customers__tags'), [
        'value', '_dlt_parent_id'
    ]) }}
),

customers as (
    {{ raw_source(source('shopify_raw', 'customers'), [
        'id', '_dlt_id'
    ]) }}
)

select
    {{ parse_gid_id('c.id') }}  as customer_id,
    t.value                     as tag
from tags t
join customers c on t._dlt_parent_id = c._dlt_id
where t.value is not null
