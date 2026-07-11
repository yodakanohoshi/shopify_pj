"""Shopify 開発ストアへ商品・顧客・割引・注文を投入する。

使い方::

    uv run python seed.py                 # 全カテゴリを順に投入
    uv run python seed.py --only discounts,orders

前提: .env に SHOPIFY_SHOP / SHOPIFY_ADMIN_TOKEN を設定済み。
API バージョンは 2025-01 を想定 (GraphQL Admin API)。
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
def seed_products(api: ShopifyAdmin) -> list[str]:
    """商品を作成し価格を設定。作成した既定バリアント ID の一覧を返す。"""
    variant_ids: list[str] = []
    for title, ptype, vendor, price, _inventory in data.PRODUCTS:
        payload = api.mutate(
            M_PRODUCT_CREATE,
            {"input": {"title": title, "productType": ptype, "vendor": vendor, "status": "ACTIVE"}},
            "productCreate",
        )
        product_id = payload["product"]["id"]
        variant_id = payload["product"]["variants"]["edges"][0]["node"]["id"]
        api.mutate(
            M_VARIANT_UPDATE,
            {"productId": product_id, "variants": [{"id": variant_id, "price": str(price)}]},
            "productVariantsBulkUpdate",
        )
        variant_ids.append(variant_id)
        print(f"  product: {title} ({price})")
    return variant_ids


def seed_customers(api: ShopifyAdmin) -> list[str]:
    customer_ids: list[str] = []
    for first, last, email, country in data.CUSTOMERS:
        payload = api.mutate(
            M_CUSTOMER_CREATE,
            {"input": {"firstName": first, "lastName": last, "email": email,
                       "addresses": [{"countryCode": country}]}},
            "customerCreate",
        )
        customer_ids.append(payload["customer"]["id"])
        print(f"  customer: {first} {last} <{email}>")
    return customer_ids


def seed_discounts(api: ShopifyAdmin) -> None:
    for d in data.DISCOUNTS:
        kind = d["kind"]
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
        default="products,customers,discounts,orders",
        help="投入カテゴリをカンマ区切りで指定 (既定: 全部)",
    )
    args = parser.parse_args()
    only = {s.strip() for s in args.only.split(",") if s.strip()}

    api = ShopifyAdmin()
    variant_ids: list[str] = []
    customer_ids: list[str] = []

    try:
        if "products" in only:
            print("[products]")
            variant_ids = seed_products(api)
        if "customers" in only:
            print("[customers]")
            customer_ids = seed_customers(api)
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
