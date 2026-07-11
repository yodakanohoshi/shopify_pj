with source as (
    select * from {{ source('shopify_raw', 'discounts__codes') }}
)

select
    id                                          as discount_code_id,
    _dlt_parent_id                              as discount_dlt_id,
    code                                        as discount_code,
    cast(async_usage_count as integer)          as code_usage_count

from source
