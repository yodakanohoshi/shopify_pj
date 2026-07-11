{#
  コレクションディメンション。所属商品数の実測も付与。1 行 = 1 コレクション。
#}

with collections as (
    select * from {{ ref('stg_shopify__collections') }}
),

member_agg as (
    select collection_id, count(*) as member_product_count
    from {{ ref('stg_shopify__collection_products') }}
    group by 1
)

select
    c.collection_id,
    c.collection_title,
    c.handle,
    c.sort_order,
    c.products_count                        as products_count_reported,
    coalesce(m.member_product_count, 0)     as products_count_actual,
    c.updated_at
from collections c
left join member_agg m on c.collection_id = m.collection_id
