# 01. raw ソーステーブル定義書

スキーマ: `raw` / 生成: `dataload/` の dlt / API: Shopify Admin GraphQL

dlt が API レスポンスを正規化して投入する。列名は snake_case、ネストは `__` 区切りで平坦化される。
全テーブルに監査列 `_dlt_id` (PK 相当・行一意)、`_dlt_load_id` が付く (以降の表では省略)。

---

## raw.orders — 注文ヘッダ

| カラム | 型 | 説明 |
|---|---|---|
| id | varchar | 注文 global ID (`gid://shopify/Order/...`)。**PK** |
| legacy_resource_id | varchar | 数値の legacy 注文 ID |
| name | varchar | 注文名 (例 `#1001`) |
| created_at / updated_at | varchar(ISO8601) | 作成 / 更新日時。updated_at は増分キー |
| processed_at / cancelled_at / closed_at | varchar | 処理 / キャンセル / クローズ日時 |
| display_financial_status | varchar | 支払ステータス (PAID, PENDING 等) |
| display_fulfillment_status | varchar | 配送ステータス (FULFILLED 等) |
| currency_code | varchar | 通貨コード |
| email / phone / note | varchar | 連絡先・備考 |
| customer__id | varchar | 注文者顧客 ID (FK → customers.id、ゲストは null) |
| total_price_set__shop_money__amount | varchar(数値) | 合計金額 |
| subtotal_price_set__shop_money__amount | varchar(数値) | 小計 |
| total_tax_set__shop_money__amount | varchar(数値) | 税額 |
| total_discounts_set__shop_money__amount | varchar(数値) | 割引総額 |
| total_shipping_price_set__shop_money__amount | varchar(数値) | 送料 |

## raw.orders__line_items — 注文明細 (orders の子)

| カラム | 型 | 説明 |
|---|---|---|
| _dlt_id | varchar | 明細行一意 ID。**PK** |
| _dlt_parent_id | varchar | 親注文の `orders._dlt_id`。**FK** |
| id | varchar | 明細 global ID |
| title | varchar | 商品名 (注文時点) |
| quantity | bigint | 数量 |
| sku / vendor | varchar | SKU / ベンダー |
| product__id | varchar | 商品 ID (FK → products.id) |
| variant__id | varchar | バリアント ID |
| original_unit_price_set__shop_money__amount | varchar(数値) | 元単価 |
| discounted_unit_price_set__shop_money__amount | varchar(数値) | 割引後単価 |
| total_discount_set__shop_money__amount | varchar(数値) | 明細割引額 |

## raw.orders__discount_applications — 注文への割引適用 (orders の子)

| カラム | 型 | 説明 |
|---|---|---|
| _dlt_id | varchar | 一意 ID。**PK** |
| _dlt_parent_id | varchar | 親注文の `orders._dlt_id`。**FK** |
| allocation_method | varchar | 配分方法 (ACROSS / EACH) |
| target_selection | varchar | 対象選択 (ALL / ENTITLED 等) |
| target_type | varchar | 対象種別 (LINE_ITEM / SHIPPING_LINE) |
| code | varchar | 割引コード (コード割引の場合) |
| title | varchar | 割引名 (自動/手動割引の場合) |
| value__amount / value__currency_code | varchar | 定額割引の額・通貨 |
| value__percentage | varchar(数値) | 定率割引の率 |

---

## raw.customers — 顧客

| カラム | 型 | 説明 |
|---|---|---|
| id | varchar | 顧客 global ID。**PK** |
| legacy_resource_id | varchar | 数値 legacy 顧客 ID |
| first_name / last_name | varchar | 氏名 |
| email / phone | varchar | 連絡先 |
| state | varchar | 顧客状態 (ENABLED, DISABLED 等) |
| verified_email | boolean | メール確認済みか |
| number_of_orders | bigint | 注文数 (API 集計値) |
| amount_spent__amount | varchar(数値) | 生涯購入額 |
| amount_spent__currency_code | varchar | 通貨 |
| default_address__city / __province / __country / __country_code_v2 / __zip | varchar | 既定住所 |
| created_at / updated_at | varchar(ISO8601) | 作成 / 更新日時 |

---

## raw.products — 商品ヘッダ

| カラム | 型 | 説明 |
|---|---|---|
| id | varchar | 商品 global ID。**PK** |
| legacy_resource_id | varchar | 数値 legacy 商品 ID |
| title / handle | varchar | 商品名 / URL ハンドル |
| product_type / vendor | varchar | 商品タイプ / ベンダー |
| status | varchar | ACTIVE / ARCHIVED / DRAFT |
| total_inventory | bigint | 総在庫数 |
| created_at / updated_at / published_at | varchar(ISO8601) | 各日時 |

## raw.products__variants — 商品バリアント (products の子)

| カラム | 型 | 説明 |
|---|---|---|
| _dlt_id | varchar | 一意 ID。**PK** |
| _dlt_parent_id | varchar | 親商品の `products._dlt_id`。**FK** |
| id | varchar | バリアント global ID |
| legacy_resource_id | varchar | 数値 legacy ID |
| title / sku / barcode | varchar | バリアント名 / SKU / バーコード |
| price / compare_at_price | varchar(数値) | 価格 / 参考価格 |
| inventory_quantity | bigint | 在庫数 |
| position | bigint | 表示順 |

---

## raw.discounts — 割引 (discountNodes ・dlt 標準非対応をカスタム取得)

`discount` フィールドをトップに引き上げ、`__typename` を `discount_type` として保持している。
コード割引と自動割引を統合。Basic 系のみ `customer_gets__value__*` に値を持つ。

| カラム | 型 | 説明 |
|---|---|---|
| id | varchar | 割引 global ID。**PK** |
| discount_type | varchar | 種別 (`DiscountCodeBasic`, `DiscountAutomaticBasic` 等) |
| title | varchar | 割引名 |
| status | varchar | ACTIVE / EXPIRED / SCHEDULED |
| summary | varchar | 割引内容の要約 |
| usage_limit | bigint | 利用上限 (コード割引) |
| applies_once_per_customer | boolean | 顧客あたり1回制限 |
| async_usage_count | bigint | 総利用回数 |
| customer_gets__value__percentage | varchar(数値) | 定率割引の率 |
| customer_gets__value__amount__amount | varchar(数値) | 定額割引の額 |
| customer_gets__value__amount__currency_code | varchar | 通貨 |
| starts_at / ends_at | varchar(ISO8601) | 有効期間 |

## raw.discounts__codes — 割引コード (discounts の子)

| カラム | 型 | 説明 |
|---|---|---|
| _dlt_id | varchar | 一意 ID。**PK** |
| _dlt_parent_id | varchar | 親割引の `discounts._dlt_id`。**FK** |
| id | varchar | コード global ID |
| code | varchar | 割引コード文字列 |
| async_usage_count | bigint | コード別利用回数 |
