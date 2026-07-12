with source as (
    {{ raw_source(source('shopify_raw', 'customers'), [
        'id', 'legacy_resource_id', 'first_name', 'last_name',
        'default_email_address__email_address', 'default_phone_number__phone_number',
        'default_email_address__marketing_state', 'default_email_address__marketing_opt_in_level',
        'verified_email', 'state', 'tax_exempt', 'locale', 'lifetime_duration',
        'can_delete', 'data_sale_opt_out', 'number_of_orders',
        'amount_spent__amount', 'amount_spent__currency_code',
        'default_address__city', 'default_address__province', 'default_address__country',
        'default_address__country_code_v2', 'default_address__zip',
        'note', 'created_at', 'updated_at'
    ]) }}
)

select
    id                                              as customer_id,
    legacy_resource_id                              as customer_legacy_id,
    first_name,
    last_name,
    default_email_address__email_address            as email,
    default_phone_number__phone_number              as phone,
    -- メール配信同意 (SUBSCRIBED / UNSUBSCRIBED / NOT_SUBSCRIBED 等)
    default_email_address__marketing_state          as email_marketing_state,
    default_email_address__marketing_opt_in_level   as email_marketing_opt_in_level,
    verified_email,
    state                                           as customer_state,
    tax_exempt,
    locale                                          as customer_locale,
    lifetime_duration,
    can_delete,
    data_sale_opt_out,
    cast(number_of_orders as integer)               as number_of_orders,
    cast(amount_spent__amount as double)            as lifetime_amount_spent,
    amount_spent__currency_code                     as amount_spent_currency,
    default_address__city                           as city,
    default_address__province                       as province,
    default_address__country                        as country,
    default_address__country_code_v2                as country_code,
    default_address__zip                            as zip,
    note,
    cast(created_at as timestamp)                   as created_at,
    cast(updated_at as timestamp)                   as updated_at

from source
