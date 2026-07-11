{#
  商品とコレクションのブリッジに双方の名称を付与した中間モデル。
  カテゴリ別ロールアップ (product_collections マート) の素地。
#}

with bridge as (
    select * from {{ ref('stg_shopify__collection_products') }}
),

collections as (
    select collection_id, collection_title, handle from {{ ref('stg_shopify__collections') }}
),

products as (
    select product_id, product_title, product_type from {{ ref('stg_shopify__products') }}
)

select
    b.collection_id,
    col.collection_title,
    col.handle              as collection_handle,
    b.product_id,
    p.product_title,
    p.product_type
from bridge b
left join collections col on b.collection_id = col.collection_id
left join products p on b.product_id = p.product_id
