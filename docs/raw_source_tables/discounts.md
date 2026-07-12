# raw.discounts

割引 (discountNodes)。取得方式: **ページング**。**dlt 標準ソース非対応**をカスタム取得。
`discount` フィールドをトップに引き上げ、`__typename` を `discount_type` として保持。
コード割引と自動割引を統合。粒度: 1 行 = 1 割引。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 割引ID | id | varchar | 割引 global ID。**PK** |
| 割引タイプ | discount_type | varchar | 種別 (`DiscountCodeBasic`, `DiscountAutomaticBasic` 等) |
| 割引名 | title | varchar | 割引名 |
| ステータス | status | varchar | ACTIVE / EXPIRED / SCHEDULED |
| 概要 | summary | varchar | 割引内容の要約 |
| 利用上限 | usage_limit | bigint | 利用上限 (コード割引) |
| 顧客あたり1回限定 | applies_once_per_customer | boolean | 顧客あたり1回制限 |
| 利用回数 | async_usage_count | bigint | 総利用回数 |
| 割引率 | customer_gets__value__percentage | varchar(数値) | 定率割引の率 |
| 割引額 | customer_gets__value__amount__amount | varchar(数値) | 定額割引の額 |
| 通貨コード | customer_gets__value__amount__currency_code | varchar | 通貨 |
| 開始日時 / 終了日時 | starts_at / ends_at | varchar(ISO8601) | 有効期間 |

子テーブル: [discounts__codes](discounts__codes.md) (_dlt_parent_id → _dlt_id)。
