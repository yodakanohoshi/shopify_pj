{#
  コレクション所属商品のブリッジ。1 行 = (コレクション × 商品)。
  id=商品gid、parent_id=コレクションgid。
#}
with source as (
    {{ raw_source(source('shopify_raw', 'collection_products'), [
        'parent_id', 'id'
    ]) }}
)

select
    {{ parse_gid_id('parent_id') }} as collection_id,
    {{ parse_gid_id('id') }}        as product_id
from source
