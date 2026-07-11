"""Shopify Admin GraphQL クエリ定義。

- ``BULK_*`` : Bulk Operations 用。ページング引数を持たず、connection は edges/node で記述。
  制約: connection 最大5・ネスト最大2階層・ノードは Node(id を持つ)必須。
- ``*_PAGINATED`` : 通常のカーソルページング用 (``first/after/query`` の3変数)。
  Bulk に載せにくい/件数の少ないソース向け。

分析に有用なソースは、dlt 標準が非対応でもここでカスタム取得する
(discounts / collections / abandoned_checkouts / locations)。
"""

# =========================================================================
# Bulk Operations 用クエリ
# =========================================================================

# --- 注文 (orders → line_items) ------------------------------------------
BULK_ORDERS = """
{
  orders {
    edges { node {
      id
      legacyResourceId
      name
      createdAt
      updatedAt
      processedAt
      cancelledAt
      closedAt
      displayFinancialStatus
      displayFulfillmentStatus
      currencyCode
      email
      phone
      note
      tags
      sourceName
      discountCodes
      customer { id }
      shippingAddress { city province country countryCodeV2 zip }
      billingAddress { city province country countryCodeV2 zip }
      totalPriceSet { shopMoney { amount currencyCode } }
      subtotalPriceSet { shopMoney { amount } }
      currentTotalPriceSet { shopMoney { amount } }
      totalTaxSet { shopMoney { amount } }
      totalDiscountsSet { shopMoney { amount } }
      totalShippingPriceSet { shopMoney { amount } }
      totalRefundedSet { shopMoney { amount } }
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
    } }
  }
}
"""

# --- 商品 (products → variants) ------------------------------------------
BULK_PRODUCTS = """
{
  products {
    edges { node {
      id
      legacyResourceId
      title
      handle
      productType
      vendor
      status
      createdAt
      updatedAt
      publishedAt
      tags
      totalInventory
      category { id name fullName }
      options { name position }
      variants {
        edges { node {
          id
          legacyResourceId
          title
          sku
          barcode
          price
          compareAtPrice
          inventoryQuantity
          position
          selectedOptions { name value }
          inventoryItem {
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
  customers {
    edges { node {
      id
      legacyResourceId
      firstName
      lastName
      note
      tags
      verifiedEmail
      state
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
  collections {
    edges { node {
      id
      title
      handle
      updatedAt
      sortOrder
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
  abandonedCheckouts {
    edges { node {
      id
      createdAt
      updatedAt
      completedAt
      abandonedCheckoutUrl
      customer { id }
      totalPriceSet { shopMoney { amount currencyCode } }
      subtotalPriceSet { shopMoney { amount } }
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
      address { city province country countryCode zip }
    } }
    pageInfo { hasNextPage endCursor }
  }
}
"""
