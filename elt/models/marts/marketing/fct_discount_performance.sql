{#
  割引パフォーマンスファクト。1 行 = 1 割引。
  利用回数・適用注文数・値引き総額から効果を評価する。
#}

with discounts as (
    select * from {{ ref('int_discounts__enriched') }}
)

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
    applied_amount_total,
    -- 利用上限に対する消化率
    case
        when usage_limit is not null and usage_limit > 0
        then round(total_usage_count::double / usage_limit, 4)
    end                                     as usage_ratio,
    starts_at,
    ends_at
from discounts
