{#
  コレクション所属商品のブリッジ。1 行 = (コレクション × 商品)。
  id=商品gid、parent_id=コレクションgid。
#}
with source as (
    select * from {{ source('shopify_raw', 'collection_products') }}
)

select
    parent_id       as collection_id,
    id              as product_id
from source
