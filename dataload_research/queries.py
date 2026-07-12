"""調査用の非 Bulk GraphQL クエリ集。

各クエリはトップレベル connection を ``first: $n`` で数件だけ取得する
(ページングしない)。**本番パイプラインには無いフィールド** (metafields / media /
options / image 等) も敢えて含め、「どんなデータが取れるか」を広く覗くのが目的。

追加/変更したいときはこの dict を編集するだけでよい。キーが ``raw_probe.py`` /
``dlt_probe.py`` の対象名になる。
"""

from __future__ import annotations

# name -> (root_field, query)。query は $n: Int! を受け取る。
PROBES: dict[str, tuple[str, str]] = {
    "orders": (
        "orders",
        """
        query($n: Int!) {
          orders(first: $n, sortKey: CREATED_AT, reverse: true) {
            edges { node {
              id name createdAt displayFinancialStatus displayFulfillmentStatus
              tags note
              totalPriceSet { shopMoney { amount currencyCode } }
              customer { id displayName }
              lineItems(first: 5) { edges { node { title quantity sku } } }
              metafields(first: 5) { edges { node { namespace key value type } } }
            } }
          }
        }
        """,
    ),
    "products": (
        "products",
        """
        query($n: Int!) {
          products(first: $n, sortKey: UPDATED_AT, reverse: true) {
            edges { node {
              id title handle productType vendor status tags
              options { name optionValues { name } }
              featuredMedia { preview { image { url } } }
              variants(first: 10) { edges { node {
                id title sku barcode price
                inventoryItem { id unitCost { amount } }
              } } }
              metafields(first: 5) { edges { node { namespace key value type } } }
            } }
          }
        }
        """,
    ),
    "customers": (
        "customers",
        """
        query($n: Int!) {
          customers(first: $n, sortKey: UPDATED_AT, reverse: true) {
            edges { node {
              id displayName tags note numberOfOrders
              amountSpent { amount currencyCode }
              defaultEmailAddress { emailAddress marketingState }
              addressesV2(first: 5) { edges { node { city country } } }
              metafields(first: 5) { edges { node { namespace key value type } } }
            } }
          }
        }
        """,
    ),
    "inventory_items": (
        "inventoryItems",
        """
        query($n: Int!) {
          inventoryItems(first: $n) {
            edges { node {
              id sku tracked requiresShipping
              unitCost { amount }
              inventoryLevels(first: 5) { edges { node {
                id location { id name }
                quantities(names: ["available","on_hand","committed","incoming"]) { name quantity }
              } } }
            } }
          }
        }
        """,
    ),
    "collections": (
        "collections",
        """
        query($n: Int!) {
          collections(first: $n) {
            edges { node {
              id title handle sortOrder productsCount { count }
              ruleSet { appliedDisjunctively rules { column relation condition } }
              products(first: 5) { edges { node { id title } } }
            } }
          }
        }
        """,
    ),
    "locations": (
        "locations",
        """
        query($n: Int!) {
          locations(first: $n) {
            edges { node {
              id name isActive fulfillsOnlineOrders
              address { city province country zip }
            } }
          }
        }
        """,
    ),
    "discount_nodes": (
        "discountNodes",
        """
        query($n: Int!) {
          discountNodes(first: $n) {
            edges { node {
              id
              discount {
                __typename
                ... on DiscountCodeBasic { title status summary asyncUsageCount }
                ... on DiscountAutomaticBasic { title status summary asyncUsageCount }
              }
            } }
          }
        }
        """,
    ),
}
