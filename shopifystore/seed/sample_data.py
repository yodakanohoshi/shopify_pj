"""投入するサンプルデータ定義。分析基盤の検証に足る多様性を持たせる。

原価 (cost) を含めることで粗利分析、コレクションでカテゴリ分析、
メール配信同意で顧客セグメント分析を検証できるようにしている。
"""

# 商品: (タイトル, 商品タイプ, ベンダー, 価格, 原価, 在庫)
PRODUCTS = [
    ("Aurora Hoodie", "Apparel", "Northlight", 6, 3, 40),
    ("Cascade Water Bottle", "Accessories", "Northlight", 5, 1, 120),
    ("Ember Scented Candle", "Home", "Hearth&Co", 7, 6, 80),
    ("Nimbus Rain Jacket", "Apparel", "Northlight", 2, 1, 25),
    ("Pebble Wireless Mouse", "Electronics", "Cobalt", 3, 2, 60),
    ("Slate Notebook A5", "Stationery", "Cobalt", 3, 2, 200),
    ("Lumen Desk Lamp", "Home", "Hearth&Co", 5, 2, 35),
    ("Terra Ceramic Mug", "Home", "Hearth&Co", 7, 5, 150),
]

# 顧客: (姓, 名, メール, 国コード, メール配信同意)
CUSTOMERS = [
    ("Yui", "Tanaka", "yui.tanaka@example.com", "JP", True),
    ("Ken", "Sato", "ken.sato@example.com", "JP", False),
    ("Emma", "Brown", "emma.brown@example.com", "US", True),
    ("Liam", "Wilson", "liam.wilson@example.com", "GB", True),
    ("Mia", "Davis", "mia.davis@example.com", "US", False),
]

# コレクション: (タイトル, [商品インデックス, ...])
COLLECTIONS = [
    ("Apparel", [0, 3]),
    ("Home & Living", [2, 6, 7]),
    ("Work Essentials", [4, 5]),
]

# 割引: kind = percentage / amount / free_shipping / automatic
DISCOUNTS = [
    {"kind": "percentage", "title": "Spring Sale 10%", "code": "SPRING10", "percentage": 0.10,
     "usage_limit": 100},
    {"kind": "amount", "title": "500 OFF Coupon", "code": "SAVE500", "amount": 1,
     "usage_limit": 50},
    {"kind": "free_shipping", "title": "Free Shipping", "code": "FREESHIP", "usage_limit": 200},
    {"kind": "automatic", "title": "Auto 5% Off", "percentage": 0.05},
]

# 注文: (顧客インデックス, [(商品インデックス, 数量), ...], 手動割引率 or None)
ORDERS = [
    (0, [(0, 1), (2, 2)], None),
    (1, [(1, 3)], 0.10),
    (2, [(3, 1), (4, 1)], None),
    (3, [(5, 1)], 0.05),
    (0, [(4, 2)], None),
    (1, [(2, 1), (5, 3)], 0.10),
    (2, [(0, 1)], None),
    (3, [(1, 2), (3, 1)], None),
    (4, [(6, 1), (7, 2)], None),
    (4, [(7, 4)], 0.05),
]
