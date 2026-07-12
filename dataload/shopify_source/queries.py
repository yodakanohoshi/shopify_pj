"""Shopify Admin GraphQL クエリ定義。

- ``BULK_*`` : Bulk Operations 用。ページング引数を持たず、connection は edges/node で記述。
  制約: connection 最大5・ネスト最大2階層・ノードは Node(id を持つ)必須。
  トップレベル connection には ``%(f)s`` プレースホルダを置き、差分取得時は
  ``build`` / ``date_filter`` で ``(query: "updated_at:>=...")`` を注入する
  (バックフィル時は空文字 → 全件エクスポート)。
- ``*_PAGINATED`` : 通常のカーソルページング用 (``first/after/query`` の3変数)。
  Bulk に載せにくい/件数の少ないソース向け。

分析に有用なソースは、dlt 標準が非対応でもここでカスタム取得する
(discounts / collections / abandoned_checkouts / locations)。
"""

from __future__ import annotations

import json


def date_filter(field: str, low: str | None = None, high: str | None = None) -> str:
    """Shopify 検索構文の ``(query: "...")`` 節を組み立てる。

    ``field`` は ``updated_at`` / ``created_at`` などの検索フィールド。境界は両端含む
    (``>=`` / ``<=``)。低境界・高境界がいずれも無ければ空文字を返し、全件取得となる。
    """
    parts = []
    if low:
        parts.append(f"{field}:>='{low}'")
    if high:
        parts.append(f"{field}:<='{high}'")
    if not parts:
        return ""
    return f"(query: {json.dumps(' AND '.join(parts))})"


def build(template: str, filter_clause: str = "") -> str:
    """``BULK_*`` テンプレートの ``%(f)s`` へ connection 引数節を差し込む。"""
    return template % {"f": filter_clause}


# =========================================================================
# Bulk Operations 用クエリ
# =========================================================================

# --- 注文 (orders → line_items) ------------------------------------------
BULK_ORDERS = """
{
  orders%(f)s {
    edges { node {
      id
      legacyResourceId
      name
      number
      confirmationNumber
      createdAt
      updatedAt
      processedAt
      cancelledAt
      closedAt
      cancelReason
      closed
      test
      taxesIncluded
      taxExempt
      displayFinancialStatus
      displayFulfillmentStatus
      currencyCode
      email
      phone
      note
      poNumber
      customerLocale
      customerAcceptsMarketing
      billingAddressMatchesShippingAddress
      subtotalLineItemsQuantity
      currentSubtotalLineItemsQuantity
      currentTotalWeight
      fulfillmentsCount { count }
      paymentGatewayNames
      tags
      sourceName
      discountCode
      discountCodes
      customer { id }
      shippingAddress { city province country countryCodeV2 zip }
      billingAddress { city province country countryCodeV2 zip }
      totalPriceSet { shopMoney { amount currencyCode } }
      subtotalPriceSet { shopMoney { amount } }
      currentTotalPriceSet { shopMoney { amount } }
      currentSubtotalPriceSet { shopMoney { amount } }
      totalTaxSet { shopMoney { amount } }
      currentTotalTaxSet { shopMoney { amount } }
      totalDiscountsSet { shopMoney { amount } }
      currentTotalDiscountsSet { shopMoney { amount } }
      totalShippingPriceSet { shopMoney { amount } }
      totalRefundedSet { shopMoney { amount } }
      netPaymentSet { shopMoney { amount } }
      lineItems {
        edges { node {
          id
          title
          quantity
          sku
          vendor
          product { id }
          variant { id }
          originalUnitPriceSet { shopMoney { amount } }
          discountedUnitPriceSet { shopMoney { amount } }
          totalDiscountSet { shopMoney { amount } }
        } }
      }
      refunds {
        id
        createdAt
        processedAt
        note
        totalRefundedSet { shopMoney { amount currencyCode } }
      }
      fulfillments {
        id
        status
        displayStatus
        createdAt
        updatedAt
        estimatedDeliveryAt
        deliveredAt
        inTransitAt
        totalQuantity
        name
      }
      transactions {
        id
        kind
        status
        gateway
        processedAt
        createdAt
        test
        amountSet { shopMoney { amount currencyCode } }
      }
    } }
  }
}
"""

# --- 商品 (products → variants) ------------------------------------------
BULK_PRODUCTS = """
{
  products%(f)s {
    edges { node {
      id
      legacyResourceId
      title
      handle
      description
      productType
      vendor
      status
      createdAt
      updatedAt
      publishedAt
      tags
      totalInventory
      tracksInventory
      hasOnlyDefaultVariant
      isGiftCard
      requiresSellingPlan
      templateSuffix
      onlineStoreUrl
      variantsCount { count }
      seo { title description }
      category { id name fullName }
      options { name position }
      variants {
        edges { node {
          id
          legacyResourceId
          title
          displayName
          sku
          barcode
          price
          compareAtPrice
          inventoryQuantity
          sellableOnlineQuantity
          availableForSale
          taxable
          inventoryPolicy
          position
          createdAt
          updatedAt
          selectedOptions { name value }
          inventoryItem {
            id
            tracked
            requiresShipping
            unitCost { amount currencyCode }
            measurement { weight { value unit } }
          }
        } }
      }
    } }
  }
}
"""

# --- 顧客 (customers → addressesV2) --------------------------------------
# email / emailMarketingConsent は非推奨のため defaultEmailAddress を使用。
BULK_CUSTOMERS = """
{
  customers%(f)s {
    edges { node {
      id
      legacyResourceId
      firstName
      lastName
      note
      tags
      verifiedEmail
      state
      taxExempt
      locale
      lifetimeDuration
      canDelete
      dataSaleOptOut
      numberOfOrders
      createdAt
      updatedAt
      amountSpent { amount currencyCode }
      defaultEmailAddress { emailAddress marketingState marketingOptInLevel }
      defaultPhoneNumber { phoneNumber }
      defaultAddress { city province country countryCodeV2 zip }
      addressesV2 {
        edges { node { id city province country countryCodeV2 zip } }
      }
    } }
  }
}
"""

# --- コレクション (collections → products membership) --------------------
BULK_COLLECTIONS = """
{
  collections%(f)s {
    edges { node {
      id
      title
      handle
      description
      templateSuffix
      updatedAt
      sortOrder
      seo { title description }
      productsCount { count }
      products {
        edges { node { id } }
      }
    } }
  }
}
"""

# --- 放棄チェックアウト (abandoned_checkouts → line_items) ---------------
# ファネル/離脱分析用。dlt 標準非対応のためカスタム取得。
BULK_ABANDONED_CHECKOUTS = """
{
  abandonedCheckouts%(f)s {
    edges { node {
      id
      createdAt
      updatedAt
      completedAt
      abandonedCheckoutUrl
      note
      taxesIncluded
      discountCodes
      customer { id }
      billingAddress { city province country countryCodeV2 zip }
      shippingAddress { city province country countryCodeV2 zip }
      totalPriceSet { shopMoney { amount currencyCode } }
      subtotalPriceSet { shopMoney { amount } }
      totalLineItemsPriceSet { shopMoney { amount } }
      totalTaxSet { shopMoney { amount } }
      totalDiscountSet { shopMoney { amount } }
      lineItems {
        edges { node {
          id
          title
          quantity
          variant { id }
          product { id }
        } }
      }
    } }
  }
}
"""


# =========================================================================
# 通常ページング用クエリ (first / after / query)
# =========================================================================

# --- 割引 (discountNodes) ------------------------------------------------
# dlt 標準非対応。コード割引・自動割引の両方を返すユニオン。
DISCOUNTS_PAGINATED = """
query Discounts($first: Int!, $after: String, $query: String) {
  discountNodes(first: $first, after: $after, query: $query) {
    edges {
      node {
        id
        discount {
          __typename
          ... on DiscountCodeBasic {
            title status summary startsAt endsAt usageLimit appliesOncePerCustomer asyncUsageCount
            codes(first: 20) { edges { node { id code asyncUsageCount } } }
            customerGets { value {
              __typename
              ... on DiscountPercentage { percentage }
              ... on DiscountAmount { amount { amount currencyCode } appliesOnEachItem }
            } }
          }
          ... on DiscountCodeBxgy {
            title status summary startsAt endsAt usageLimit asyncUsageCount
            codes(first: 20) { edges { node { id code asyncUsageCount } } }
          }
          ... on DiscountCodeFreeShipping {
            title status summary startsAt endsAt usageLimit asyncUsageCount
            codes(first: 20) { edges { node { id code asyncUsageCount } } }
          }
          ... on DiscountAutomaticBasic {
            title status summary startsAt endsAt asyncUsageCount
            customerGets { value {
              __typename
              ... on DiscountPercentage { percentage }
              ... on DiscountAmount { amount { amount currencyCode } appliesOnEachItem }
            } }
          }
          ... on DiscountAutomaticBxgy { title status summary startsAt endsAt asyncUsageCount }
          ... on DiscountAutomaticFreeShipping { title status summary startsAt endsAt asyncUsageCount }
        }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""

# --- ロケーション (locations) --------------------------------------------
LOCATIONS_PAGINATED = """
query Locations($first: Int!, $after: String, $query: String) {
  locations(first: $first, after: $after, query: $query) {
    edges { node {
      id
      legacyResourceId
      name
      isActive
      fulfillsOnlineOrders
      shipsInventory
      hasActiveInventory
      address {
        address1 address2 city province provinceCode
        country countryCode zip phone latitude longitude
      }
    } }
    pageInfo { hasNextPage endCursor }
  }
}
"""


# --- 在庫レベル (locations → inventoryLevels) ----------------------------
# ロケーション×在庫アイテムの在庫数スナップショット。Bulk で全件取得する。
# InventoryLevel ノードは __parentId に location gid を持ち、item.id で
# product_variants.inventory_item__id と結合できる。quantities は必須引数
# names を取り、name/quantity のペアが inventory_levels__quantities 子へ展開される。
BULK_INVENTORY_LEVELS = """
{
  locations {
    edges { node {
      id
      inventoryLevels {
        edges { node {
          id
          item { id sku }
          quantities(names: ["available", "on_hand", "committed", "incoming"]) {
            name
            quantity
          }
        } }
      }
    } }
  }
}
"""
