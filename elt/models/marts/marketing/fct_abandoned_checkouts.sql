{#
  放棄チェックアウトファクト。1 行 = 1 チェックアウト。
  カゴ落ち金額・復帰率などファネル分析に使う。
#}

select
    checkout_id,
    customer_id,
    checkout_date,
    currency_code,
    line_count,
    total_quantity,
    subtotal_price,
    total_price,
    is_recovered,
    created_at,
    completed_at
from {{ ref('int_abandoned_checkouts__enriched') }}
