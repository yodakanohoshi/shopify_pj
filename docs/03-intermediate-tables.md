# 03. intermediate テーブル定義書

スキーマ: `intermediate` / 生成: `elt/` dbt (materialized: **view**) / 命名: `int_<entity>__<verb>`

staging を結合・集計した中間表現。marts の素地であり、原則 BI から直接参照しない。

---

## intermediate.int_orders__enriched — 注文 + 明細集計 + 顧客属性

粒度: 1 行 = 1 注文。

| カラム | 型 | 説明 |
|---|---|---|
| order_id | varchar | 注文 ID。**PK** |
| order_name / order_legacy_id | varchar | 注文名 / legacy ID |
| customer_id | varchar | 顧客 ID (FK) |
| customer_email / customer_country | varchar | 顧客の付帯情報 (結合) |
| financial_status / fulfillment_status | varchar | ステータス |
| currency_code | varchar | 通貨 |
| total_price / subtotal_price / total_tax / total_discounts / total_shipping | double | 各金額 |
| line_count | integer | 明細数 (集計) |
| total_quantity | integer | 合計数量 (集計) |
| line_discount_total | double | 明細割引の合計 (集計) |
| order_date | date | 注文日 (created_at の日付) |
| is_cancelled | boolean | キャンセル済みか |
| created_at / processed_at / cancelled_at | timestamp | 各日時 |

## intermediate.int_order_lines__enriched — 明細 + 注文日 + 商品属性

粒度: 1 行 = 1 明細。

| カラム | 型 | 説明 |
|---|---|---|
| order_line_id | varchar | 明細 ID。**PK** |
| order_id | varchar | 注文 ID (FK、注文サロゲート経由で解決) |
| product_id / variant_id | varchar | 商品 / バリアント ID |
| product_title | varchar | 商品名 (商品マスタ優先、無ければ注文時点名) |
| product_type / vendor | varchar | 商品属性 (結合) |
| sku | varchar | SKU |
| quantity | integer | 数量 |
| original_unit_price / discounted_unit_price / line_discount | double | 単価・割引 |
| net_line_revenue | double | 純売上 = 割引後単価 × 数量 |
| currency_code | varchar | 通貨 |
| financial_status | varchar | 注文の支払ステータス |
| order_date | date | 注文日 |

## intermediate.int_discounts__enriched — 割引 + コード集計 + 適用実績

粒度: 1 行 = 1 割引。

| カラム | 型 | 説明 |
|---|---|---|
| discount_id | varchar | 割引 ID。**PK** |
| discount_type / discount_method | varchar | 種別 / 手法 |
| discount_title / discount_status | varchar | 名称 / 状態 |
| discount_percentage / discount_amount / discount_currency | double / varchar | 割引値 |
| usage_limit | integer | 利用上限 |
| total_usage_count | integer | 総利用回数 (API 値) |
| code_count | integer | 紐づくコード数 (集計) |
| code_usage_total | integer | コード利用回数の合計 (集計) |
| sample_code | varchar | 代表コード (突合用) |
| orders_with_code | integer | そのコードが使われた注文数 (実績) |
| applied_amount_total | double | 実際に値引きされた総額 (実績) |
| starts_at / ends_at | timestamp | 有効期間 |

> `orders_with_code` / `applied_amount_total` は `stg_shopify__order_discount_applications` をコード文字列で突合した実績値。複数コードを持つ割引では代表コード基準の近似となる。
