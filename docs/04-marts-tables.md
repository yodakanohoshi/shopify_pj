# 04. marts テーブル定義書

スキーマ: `marts` / 生成: `elt/` dbt (materialized: **table**) / 命名: `dim_` / `fct_`

分析・BI が参照する最終形。ディメンション (dim) とファクト (fct) で構成する。

---

## marts.dim_customers — 顧客ディメンション

粒度: 1 行 = 1 顧客。属性 + 実注文からの集計指標。

| カラム | 型 | 説明 |
|---|---|---|
| customer_id | varchar | 顧客 ID。**PK** |
| customer_legacy_id | varchar | 数値 legacy ID |
| first_name / last_name / email | varchar | 氏名・メール |
| customer_state | varchar | 顧客状態 |
| country / country_code / city | varchar | 所在地 |
| lifetime_amount_spent | double | 生涯購入額 (API 値) |
| orders_count | integer | 注文数 (キャンセル除く実績集計) |
| revenue_total | double | 売上合計 (キャンセル除く) |
| first_order_date / latest_order_date | date | 初回 / 最新注文日 |
| created_at / updated_at | timestamp | 各日時 |

## marts.dim_products — 商品ディメンション

粒度: 1 行 = 1 商品。バリアントの価格レンジ・在庫を集約。

| カラム | 型 | 説明 |
|---|---|---|
| product_id | varchar | 商品 ID。**PK** |
| product_legacy_id | varchar | 数値 legacy ID |
| product_title / handle | varchar | 商品名 / ハンドル |
| product_type / vendor | varchar | タイプ / ベンダー |
| product_status | varchar | ACTIVE / ARCHIVED / DRAFT |
| variant_count | integer | バリアント数 |
| min_price / max_price | double | 価格レンジ |
| total_inventory | integer | 総在庫 (バリアント集計、無ければ商品値) |
| created_at / published_at | timestamp | 作成 / 公開日時 |

---

## marts.fct_orders — 注文ファクト

粒度: 1 行 = 1 注文。売上・AOV 分析の基点。

| カラム | 型 | 説明 |
|---|---|---|
| order_id | varchar | 注文 ID。**PK** |
| order_name | varchar | 注文名 |
| customer_id | varchar | 顧客 ID。**FK → dim_customers** (ゲストは null) |
| order_date | date | 注文日 |
| financial_status / fulfillment_status | varchar | ステータス |
| is_cancelled | boolean | キャンセル済みか |
| currency_code | varchar | 通貨 |
| line_count / total_quantity | integer | 明細数 / 合計数量 |
| subtotal_price / total_discounts / total_tax / total_shipping / total_price | double | 各金額 |
| net_revenue | double | 純売上 = 小計 − 割引 |
| created_at / processed_at | timestamp | 各日時 |

## marts.fct_order_lines — 注文明細ファクト

粒度: 1 行 = 1 明細。商品別・カテゴリ別売上分析。

| カラム | 型 | 説明 |
|---|---|---|
| order_line_id | varchar | 明細 ID。**PK** |
| order_id | varchar | 注文 ID。**FK → fct_orders** |
| product_id / variant_id | varchar | 商品 / バリアント ID |
| product_title / product_type / vendor | varchar | 商品属性 |
| sku | varchar | SKU |
| order_date | date | 注文日 |
| quantity | integer | 数量 |
| original_unit_price / discounted_unit_price / line_discount | double | 単価・割引 |
| net_line_revenue | double | 純売上 = 割引後単価 × 数量 |
| currency_code | varchar | 通貨 |

---

## marts.fct_discount_performance — 割引パフォーマンスファクト

粒度: 1 行 = 1 割引。利用状況・値引き効果を評価 (marketing 配下)。

| カラム | 型 | 説明 |
|---|---|---|
| discount_id | varchar | 割引 ID。**PK** |
| discount_title | varchar | 割引名 |
| discount_type / discount_method | varchar | 種別 / 手法 (code / automatic) |
| discount_status | varchar | 状態 |
| discount_percentage / discount_amount / discount_currency | double / varchar | 割引値 |
| usage_limit | integer | 利用上限 |
| total_usage_count | integer | 総利用回数 |
| code_count / code_usage_total | integer | コード数 / コード利用合計 |
| sample_code | varchar | 代表コード |
| orders_with_code | integer | 適用注文数 (実績) |
| applied_amount_total | double | 値引き総額 (実績) |
| usage_ratio | double | 利用上限消化率 = total_usage_count / usage_limit |
| starts_at / ends_at | timestamp | 有効期間 |

---

## 分析クエリ例

```sql
-- 月次売上と AOV
select date_trunc('month', order_date) as month,
       count(*) as orders, sum(net_revenue) as revenue,
       avg(net_revenue) as aov
from marts.fct_orders
where not is_cancelled
group by 1 order by 1;

-- 商品別売上 Top10
select product_title, sum(net_line_revenue) as revenue, sum(quantity) as qty
from marts.fct_order_lines
group by 1 order by revenue desc limit 10;

-- 割引効果ランキング
select discount_title, orders_with_code, applied_amount_total, usage_ratio
from marts.fct_discount_performance
order by applied_amount_total desc;
```
