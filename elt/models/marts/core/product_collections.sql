{#
  商品×コレクションのブリッジマート。カテゴリ別売上ロールアップに使う。
  1 行 = (コレクション × 商品)。
#}

select
    collection_id,
    collection_title,
    collection_handle,
    product_id,
    product_title,
    product_type
from {{ ref('int_product_collections') }}
