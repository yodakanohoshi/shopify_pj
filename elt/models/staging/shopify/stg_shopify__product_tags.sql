{#
  商品タグ (long 形式)。1 行 = (商品 × タグ)。

  Shopify の product.tags は [String!]! (scalar のリスト)。dlt はこれを
  子テーブル products__tags (値は value 列) へ正規化する。親への参照は
  gid ではなく dlt 内部行 ID (_dlt_parent_id → products._dlt_id) なので、
  raw products と結合して商品 gid を取り出し、数値 ID へ変換する。
#}
with tags as (
    {{ raw_source(source('shopify_raw', 'products__tags'), [
        'value', '_dlt_parent_id'
    ]) }}
),

products as (
    {{ raw_source(source('shopify_raw', 'products'), [
        'id', '_dlt_id'
    ]) }}
)

select
    {{ parse_gid_id('p.id') }}  as product_id,
    t.value                     as tag
from tags t
join products p on t._dlt_parent_id = p._dlt_id
where t.value is not null
