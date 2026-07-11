"""Shopify Admin GraphQL クエリ定義。

すべて `first / after / query` の3変数でカーソルページングできる形に統一している。
`query` 変数には Shopify の検索構文 (例: ``updated_at:>=2024-01-01``) を渡し、
増分ロード (incremental) のフィルタとして利用する。
"""

# --- 注文 (orders) --------------------------------------------------------
# lineItems / discountApplications など分析でよく使うネストも同時取得する。
ORDERS = """
query Orders($first: Int!, $after: String, $query: String) {
  orders(first: $first, after: $after, query: $query, sortKey: UPDATED_AT) {
    edges {
      node {
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
        totalPriceSet { shopMoney { amount currencyCode } }
        subtotalPriceSet { shopMoney { amount currencyCode } }
        totalTaxSet { shopMoney { amount currencyCode } }
        totalDiscountsSet { shopMoney { amount currencyCode } }
        totalShippingPriceSet { shopMoney { amount currencyCode } }
        customer { id legacyResourceId }
        lineItems(first: 100) {
          edges {
            node {
              id
              title
              quantity
              sku
              vendor
              originalUnitPriceSet { shopMoney { amount currencyCode } }
              discountedUnitPriceSet { shopMoney { amount currencyCode } }
              totalDiscountSet { shopMoney { amount currencyCode } }
              product { id legacyResourceId }
              variant { id legacyResourceId }
            }
          }
        }
        discountApplications(first: 20) {
          edges {
            node {
              __typename
              allocationMethod
              targetSelection
              targetType
              value {
                __typename
                ... on MoneyV2 { amount currencyCode }
                ... on PricingPercentageValue { percentage }
              }
              ... on DiscountCodeApplication { code }
              ... on AutomaticDiscountApplication { title }
              ... on ManualDiscountApplication { title description }
            }
          }
        }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""

# --- 顧客 (customers) -----------------------------------------------------
CUSTOMERS = """
query Customers($first: Int!, $after: String, $query: String) {
  customers(first: $first, after: $after, query: $query, sortKey: UPDATED_AT) {
    edges {
      node {
        id
        legacyResourceId
        createdAt
        updatedAt
        firstName
        lastName
        email
        phone
        note
        tags
        state
        verifiedEmail
        numberOfOrders
        amountSpent { amount currencyCode }
        defaultAddress { city province country countryCodeV2 zip }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""

# --- 商品 / バリアント (products) ----------------------------------------
PRODUCTS = """
query Products($first: Int!, $after: String, $query: String) {
  products(first: $first, after: $after, query: $query, sortKey: UPDATED_AT) {
    edges {
      node {
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
        variants(first: 100) {
          edges {
            node {
              id
              legacyResourceId
              title
              sku
              barcode
              price
              compareAtPrice
              inventoryQuantity
              position
              createdAt
              updatedAt
            }
          }
        }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""

# --- 割引 (discounts) -----------------------------------------------------
# dlt 標準ソース非対応。discountNodes はコード割引・自動割引の両方を返すユニオン。
# 主要な型に inline fragment を張り、共通メタ (status / usageLimit など) を取得する。
DISCOUNTS = """
query Discounts($first: Int!, $after: String, $query: String) {
  discountNodes(first: $first, after: $after, query: $query) {
    edges {
      node {
        id
        discount {
          __typename
          ... on DiscountCodeBasic {
            title
            status
            summary
            startsAt
            endsAt
            usageLimit
            appliesOncePerCustomer
            asyncUsageCount
            codes(first: 20) { edges { node { id code asyncUsageCount } } }
            customerGets {
              value {
                __typename
                ... on DiscountPercentage { percentage }
                ... on DiscountAmount { amount { amount currencyCode } appliesOnEachItem }
              }
            }
          }
          ... on DiscountCodeBxgy {
            title
            status
            summary
            startsAt
            endsAt
            usageLimit
            asyncUsageCount
            codes(first: 20) { edges { node { id code asyncUsageCount } } }
          }
          ... on DiscountCodeFreeShipping {
            title
            status
            summary
            startsAt
            endsAt
            usageLimit
            asyncUsageCount
            codes(first: 20) { edges { node { id code asyncUsageCount } } }
          }
          ... on DiscountAutomaticBasic {
            title
            status
            summary
            startsAt
            endsAt
            asyncUsageCount
            customerGets {
              value {
                __typename
                ... on DiscountPercentage { percentage }
                ... on DiscountAmount { amount { amount currencyCode } appliesOnEachItem }
              }
            }
          }
          ... on DiscountAutomaticBxgy {
            title
            status
            summary
            startsAt
            endsAt
            asyncUsageCount
          }
          ... on DiscountAutomaticFreeShipping {
            title
            status
            summary
            startsAt
            endsAt
            asyncUsageCount
          }
        }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""
