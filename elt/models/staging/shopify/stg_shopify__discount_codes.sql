with source as (
    {{ raw_source(source('shopify_raw', 'discounts__codes'), [
        'id',
        '_dlt_parent_id',
        'code',
        'async_usage_count'
    ]) }}
)

select
    {{ parse_gid_id('id') }}                    as discount_code_id,
    _dlt_parent_id                              as discount_dlt_id,
    code                                        as discount_code,
    cast(async_usage_count as integer)          as code_usage_count

from source
