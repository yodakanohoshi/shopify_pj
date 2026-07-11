{#
  割引パフォーマンスファクト。1 行 = 1 割引。利用状況・適用注文数を評価。
#}

select
    discount_id,
    discount_title,
    discount_type,
    discount_method,
    discount_status,
    discount_percentage,
    discount_amount,
    discount_currency,
    usage_limit,
    total_usage_count,
    code_count,
    code_usage_total,
    sample_code,
    orders_with_code,
    case
        when usage_limit is not null and usage_limit > 0
        then round(total_usage_count::double / usage_limit, 4)
    end                             as usage_ratio,
    starts_at,
    ends_at
from {{ ref('int_discounts__enriched') }}
