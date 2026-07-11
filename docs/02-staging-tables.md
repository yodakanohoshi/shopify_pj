# 02. staging テーブル定義書

スキーマ: `staging` / 生成: `elt/` dbt (materialized: **view**) / 命名: `stg_<source>__<entity>`

raw を 1:1 でクレンジング (型付け・リネーム・金額の数値化) した層。ビジネスロジックは持たない。
子テーブルとの結合用に、親側は `*_dlt_id` (= raw の `_dlt_id`) を保持する。

---

## staging.stg_shopify__orders

| カラム | 型 | 説明 |
|---|---|---|
| order_id | varchar | 注文 ID。**PK** |
| order_legacy_id | varchar | 数値 legacy 注文 ID |
| order_name | varchar | 注文名 (`#1001`) |
| customer_id | varchar | 顧客 ID (FK、ゲストは null) |
| financial_status / fulfillment_status | varchar | 支払 / 配送ステータス |
| currency_code | varchar | 通貨 |
| email / phone / note | varchar | 連絡先・備考 |
| total_price / subtotal_price / total_tax / total_discounts / total_shipping | double | 各金額 (数値化済み) |
| created_at / updated_at / processed_at / cancelled_at / closed_at | timestamp | 各日時 |
| order_dlt_id | varchar | 子テーブル結合用サロゲート |

## staging.stg_shopify__order_lines

| カラム | 型 | 説明 |
|---|---|---|
| order_line_id | varchar | 明細一意 ID。**PK** |
| order_dlt_id | varchar | 親注文サロゲート (FK → stg_shopify__orders.order_dlt_id) |
| line_item_gid | varchar | 明細 global ID |
| product_id / variant_id | varchar | 商品 / バリアント ID |
| product_title | varchar | 注文時点の商品名 |
| sku / vendor | varchar | SKU / ベンダー |
| quantity | integer | 数量 |
| original_unit_price / discounted_unit_price / line_discount | double | 元単価 / 割引後単価 / 明細割引額 |

## staging.stg_shopify__order_discount_applications

| カラム | 型 | 説明 |
|---|---|---|
| order_discount_id | varchar | 一意 ID。**PK** |
| order_dlt_id | varchar | 親注文サロゲート。**FK** |
| discount_code | varchar | 割引コード |
| discount_title | varchar | 割引名 |
| allocation_method / target_selection / target_type | varchar | 配分・対象条件 |
| discount_amount / discount_currency | double / varchar | 定額割引の額・通貨 |
| discount_percentage | double | 定率割引の率 |

---

## staging.stg_shopify__customers

| カラム | 型 | 説明 |
|---|---|---|
| customer_id | varchar | 顧客 ID。**PK** |
| customer_legacy_id | varchar | 数値 legacy ID |
| first_name / last_name / email / phone | varchar | 氏名・連絡先 |
| customer_state | varchar | 顧客状態 |
| verified_email | boolean | メール確認済みか |
| number_of_orders | integer | 注文数 (API 集計値) |
| lifetime_amount_spent / amount_spent_currency | double / varchar | 生涯購入額・通貨 |
| city / province / country / country_code / zip | varchar | 既定住所 |
| created_at / updated_at | timestamp | 各日時 |

---

## staging.stg_shopify__products

| カラム | 型 | 説明 |
|---|---|---|
| product_id | varchar | 商品 ID。**PK** |
| product_legacy_id | varchar | 数値 legacy ID |
| product_title / handle | varchar | 商品名 / ハンドル |
| product_type / vendor | varchar | タイプ / ベンダー |
| product_status | varchar | ACTIVE / ARCHIVED / DRAFT |
| total_inventory | integer | 総在庫 |
| created_at / updated_at / published_at | timestamp | 各日時 |
| product_dlt_id | varchar | バリアント結合用サロゲート |

## staging.stg_shopify__product_variants

| カラム | 型 | 説明 |
|---|---|---|
| variant_id | varchar | バリアント ID。**PK** |
| variant_legacy_id | varchar | 数値 legacy ID |
| product_dlt_id | varchar | 親商品サロゲート。**FK** |
| variant_title / sku / barcode | varchar | 名称・SKU・バーコード |
| price / compare_at_price | double | 価格 / 参考価格 |
| inventory_quantity | integer | 在庫数 |
| position | integer | 表示順 |
| created_at / updated_at | timestamp | 各日時 |

---

## staging.stg_shopify__discounts

| カラム | 型 | 説明 |
|---|---|---|
| discount_id | varchar | 割引 ID。**PK** |
| discount_type | varchar | Shopify 種別名 |
| discount_method | varchar | `code` / `automatic` / `other` (種別から判定) |
| discount_title | varchar | 割引名 |
| discount_status | varchar | ACTIVE / EXPIRED / SCHEDULED |
| summary | varchar | 内容要約 |
| usage_limit | integer | 利用上限 |
| applies_once_per_customer | boolean | 顧客あたり1回制限 |
| total_usage_count | integer | 総利用回数 |
| discount_percentage / discount_amount / discount_currency | double / varchar | 割引値 (定率 / 定額) |
| starts_at / ends_at | timestamp | 有効期間 |
| discount_dlt_id | varchar | コード結合用サロゲート |

## staging.stg_shopify__discount_codes

| カラム | 型 | 説明 |
|---|---|---|
| discount_code_id | varchar | コード ID。**PK** |
| discount_dlt_id | varchar | 親割引サロゲート。**FK** |
| discount_code | varchar | コード文字列 |
| code_usage_count | integer | コード別利用回数 |
