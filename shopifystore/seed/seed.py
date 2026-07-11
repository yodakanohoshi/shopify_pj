"""Shopify 開発ストアへ商品・顧客・コレクション・割引・注文を投入する。

使い方::

    uv run python seed.py                 # 全カテゴリを順に投入
    uv run python seed.py --only products,customers,collections,discounts,orders

前提: .env に SHOPIFY_SHOP と、認証情報 (SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET
もしくは SHOPIFY_ADMIN_TOKEN) を設定済み。
API バージョンは 2025-01 を想定 (GraphQL Admin API)。

投入されるデータは分析基盤 (dataload/elt) の検証を意図している:
- 商品に原価 (cost) → 粗利分析
- コレクション → カテゴリ分析
- メール配信同意 → 顧客セグメント分析
- 割引4種 + 注文 → 売上・割引分析
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

from client import ShopifyAdmin, UserError
import sample_data as data

NOW_ISO = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

# --- GraphQL mutations ----------------------------------------------------
M_PRODUCT_CREATE = """
mutation productCreate($input: ProductInput!) {
  productCreate(input: $input) {
    product { id title variants(first: 1) { edges { node { id } } } }
    userErrors { field message }
  }
}
"""

# price と原価 (inventoryItem.cost) を同時に設定
M_VARIANT_UPDATE = """
mutation productVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(productId: $productId, variants: $variants) {
    productVariants { id price }
    userErrors { field message }
  }
}
"""

M_CUSTOMER_CREATE = """
mutation customerCreate($input: CustomerInput!) {
  customerCreate(input: $input) {
    customer { id }
    userErrors { field message }
  }
}
"""

M_EMAIL_CONSENT = """
mutation customerEmailMarketingConsentUpdate($input: CustomerEmailMarketingConsentUpdateInput!) {
  customerEmailMarketingConsentUpdate(input: $input) {
    userErrors { field message }
  }
}
"""

M_COLLECTION_CREATE = """
mutation collectionCreate($input: CollectionInput!) {
  collectionCreate(input: $input) {
    collection { id }
    userErrors { field message }
  }
}
"""

M_COLLECTION_ADD = """
mutation collectionAddProducts($id: ID!, $productIds: [ID!]!) {
  collectionAddProducts(id: $id, productIds: $productIds) {
    collection { id }
    userErrors { field message }
  }
}
"""

M_DISCOUNT_CODE_BASIC = """
mutation discountCodeBasicCreate($basicCodeDiscount: DiscountCodeBasicInput!) {
  discountCodeBasicCreate(basicCodeDiscount: $basicCodeDiscount) {
    codeDiscountNode { id }
    userErrors { field message }
  }
}
"""

M_DISCOUNT_FREE_SHIP = """
mutation discountCodeFreeShippingCreate($freeShippingCodeDiscount: DiscountCodeFreeShippingInput!) {
  discountCodeFreeShippingCreate(freeShippingCodeDiscount: $freeShippingCodeDiscount) {
    codeDiscountNode { id }
    userErrors { field message }
  }
}
"""

M_DISCOUNT_AUTOMATIC = """
mutation discountAutomaticBasicCreate($automaticBasicDiscount: DiscountAutomaticBasicInput!) {
  discountAutomaticBasicCreate(automaticBasicDiscount: $automaticBasicDiscount) {
    automaticDiscountNode { id }
    userErrors { field message }
  }
}
"""

M_DRAFT_CREATE = """
mutation draftOrderCreate($input: DraftOrderInput!) {
  draftOrderCreate(input: $input) {
    draftOrder { id }
    userErrors { field message }
  }
}
"""

M_DRAFT_COMPLETE = """
mutation draftOrderComplete($id: ID!) {
  draftOrderComplete(id: $id, paymentPending: true) {
    draftOrder { order { id name } }
    userErrors { field message }
  }
}
"""


# --- seed 各カテゴリ ------------------------------------------------------
# --- 冪等化ヘルパー (再実行で既存レコードを再利用/スキップ) ---------------
Q_FIND_PRODUCT = """
query findProduct($q: String!) {
  products(first: 1, query: $q) {
    edges { node { id variants(first: 1) { edges { node { id } } } } }
  }
}
"""

Q_FIND_CUSTOMER = """
query findCustomer($q: String!) {
  customers(first: 1, query: $q) { edges { node { id } } }
}
"""

Q_FIND_COLLECTION = """
query findCollection($q: String!) {
  collections(first: 1, query: $q) { edges { node { id } } }
}
"""


def _first_node(api: ShopifyAdmin, query: str, query_str: str) -> dict | None:
    """検索クエリの最初のノードを返す (無ければ None)。"""
    data = api.execute(query, {"q": query_str})
    edges = next(iter(data.values()))["edges"]
    return edges[0]["node"] if edges else None


def _is_duplicate(err: Exception) -> bool:
    m = str(err).lower()
    return "taken" in m or "already" in m or "exists" in m


def seed_products(api: ShopifyAdmin) -> tuple[list[str], list[str]]:
    """商品を作成し価格と原価を設定。既存 (同名) は再利用。(product_ids, variant_ids) を返す。"""
    product_ids: list[str] = []
    variant_ids: list[str] = []
    for title, ptype, vendor, price, cost, _inventory in data.PRODUCTS:
        existing = _first_node(api, Q_FIND_PRODUCT, f'title:"{title}"')
        if existing:
            product_ids.append(existing["id"])
            variant_ids.append(existing["variants"]["edges"][0]["node"]["id"])
            print(f"  product: {title} (既存を再利用)")
            continue
        payload = api.mutate(
            M_PRODUCT_CREATE,
            {"input": {"title": title, "productType": ptype, "vendor": vendor, "status": "ACTIVE"}},
            "productCreate",
        )
        product_id = payload["product"]["id"]
        variant_id = payload["product"]["variants"]["edges"][0]["node"]["id"]
        api.mutate(
            M_VARIANT_UPDATE,
            {"productId": product_id, "variants": [{
                "id": variant_id,
                "price": str(price),
                "inventoryItem": {"cost": str(cost)},
            }]},
            "productVariantsBulkUpdate",
        )
        product_ids.append(product_id)
        variant_ids.append(variant_id)
        print(f"  product: {title} (price={price}, cost={cost})")
    return product_ids, variant_ids


def seed_customers(api: ShopifyAdmin) -> list[str]:
    customer_ids: list[str] = []
    for first, last, email, country, subscribed in data.CUSTOMERS:
        existing = _first_node(api, Q_FIND_CUSTOMER, f"email:{email}")
        if existing:
            customer_ids.append(existing["id"])
            print(f"  customer: <{email}> (既存を再利用)")
            continue
        payload = api.mutate(
            M_CUSTOMER_CREATE,
            {"input": {"firstName": first, "lastName": last, "email": email,
                       "addresses": [{"countryCode": country}]}},
            "customerCreate",
        )
        cid = payload["customer"]["id"]
        customer_ids.append(cid)
        if subscribed:
            api.mutate(M_EMAIL_CONSENT, {"input": {
                "customerId": cid,
                "emailMarketingConsent": {
                    "marketingState": "SUBSCRIBED",
                    "marketingOptInLevel": "SINGLE_OPT_IN",
                },
            }}, "customerEmailMarketingConsentUpdate")
        print(f"  customer: {first} {last} <{email}> subscribed={subscribed}")
    return customer_ids


def seed_collections(api: ShopifyAdmin, product_ids: list[str]) -> None:
    if not product_ids:
        print("  [skip] collections には products の投入が必要です")
        return
    for title, product_idxs in data.COLLECTIONS:
        existing = _first_node(api, Q_FIND_COLLECTION, f'title:"{title}"')
        if existing:
            cid = existing["id"]
        else:
            cid = api.mutate(
                M_COLLECTION_CREATE, {"input": {"title": title}}, "collectionCreate"
            )["collection"]["id"]
        ids = [product_ids[i] for i in product_idxs]
        # 既に所属済みの商品を再追加しても no-op
        api.mutate(M_COLLECTION_ADD, {"id": cid, "productIds": ids}, "collectionAddProducts")
        print(f"  collection: {title} ({len(ids)} products)")


def seed_discounts(api: ShopifyAdmin) -> None:
    for d in data.DISCOUNTS:
        kind = d["kind"]
        try:
            if kind == "percentage":
                api.mutate(M_DISCOUNT_CODE_BASIC, {"basicCodeDiscount": {
                    "title": d["title"], "code": d["code"], "startsAt": NOW_ISO,
                    "usageLimit": d.get("usage_limit"), "appliesOncePerCustomer": False,
                    "customerSelection": {"all": True},
                    "customerGets": {"value": {"percentage": d["percentage"]}, "items": {"all": True}},
                }}, "discountCodeBasicCreate")
            elif kind == "amount":
                api.mutate(M_DISCOUNT_CODE_BASIC, {"basicCodeDiscount": {
                    "title": d["title"], "code": d["code"], "startsAt": NOW_ISO,
                    "usageLimit": d.get("usage_limit"), "appliesOncePerCustomer": False,
                    "customerSelection": {"all": True},
                    "customerGets": {
                        "value": {"discountAmount": {"amount": str(d["amount"]), "appliesOnEachItem": False}},
                        "items": {"all": True},
                    },
                }}, "discountCodeBasicCreate")
            elif kind == "free_shipping":
                api.mutate(M_DISCOUNT_FREE_SHIP, {"freeShippingCodeDiscount": {
                    "title": d["title"], "code": d["code"], "startsAt": NOW_ISO,
                    "usageLimit": d.get("usage_limit"), "appliesOncePerCustomer": False,
                    "customerSelection": {"all": True}, "destination": {"all": True},
                }}, "discountCodeFreeShippingCreate")
            elif kind == "automatic":
                api.mutate(M_DISCOUNT_AUTOMATIC, {"automaticBasicDiscount": {
                    "title": d["title"], "startsAt": NOW_ISO,
                    "customerGets": {"value": {"percentage": d["percentage"]}, "items": {"all": True}},
                }}, "discountAutomaticBasicCreate")
            print(f"  discount: {d['title']} ({kind})")
        except UserError as e:
            if _is_duplicate(e):
                print(f"  discount: {d['title']} (既存のためスキップ)")
            else:
                raise


def seed_orders(api: ShopifyAdmin, variant_ids: list[str], customer_ids: list[str]) -> None:
    if not variant_ids or not customer_ids:
        print("  [skip] orders には products と customers の投入が必要です")
        return
    for cust_idx, items, manual_pct in data.ORDERS:
        line_items = [{"variantId": variant_ids[pi], "quantity": qty} for pi, qty in items]
        order_input = {
            "lineItems": line_items,
            "purchasingEntity": {"customerId": customer_ids[cust_idx]},
        }
        if manual_pct:
            order_input["appliedDiscount"] = {
                "valueType": "PERCENTAGE", "value": manual_pct * 100, "title": "Seed Manual Discount",
            }
        draft = api.mutate(M_DRAFT_CREATE, {"input": order_input}, "draftOrderCreate")
        completed = api.mutate(M_DRAFT_COMPLETE, {"id": draft["draftOrder"]["id"]}, "draftOrderComplete")
        name = completed["draftOrder"]["order"]["name"]
        print(f"  order: {name} ({len(line_items)} lines)")


# --- entrypoint -----------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Shopify 開発ストアへのシード投入")
    parser.add_argument(
        "--only",
        default="products,customers,collections,discounts,orders",
        help="投入カテゴリをカンマ区切りで指定 (既定: 全部)",
    )
    args = parser.parse_args()
    only = {s.strip() for s in args.only.split(",") if s.strip()}

    api = ShopifyAdmin()
    product_ids: list[str] = []
    variant_ids: list[str] = []
    customer_ids: list[str] = []

    try:
        if "products" in only:
            print("[products]")
            product_ids, variant_ids = seed_products(api)
        if "customers" in only:
            print("[customers]")
            customer_ids = seed_customers(api)
        if "collections" in only:
            print("[collections]")
            seed_collections(api, product_ids)
        if "discounts" in only:
            print("[discounts]")
            seed_discounts(api)
        if "orders" in only:
            print("[orders]")
            seed_orders(api, variant_ids, customer_ids)
    except UserError as e:
        raise SystemExit(f"投入エラー: {e}")

    print("完了。dataload/ でパイプラインを実行してください。")


if __name__ == "__main__":
    main()
