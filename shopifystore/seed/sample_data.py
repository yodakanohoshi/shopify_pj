"""投入するサンプルデータ定義。分析基盤の検証に足る最小限の多様性を持たせる。"""

# 商品: (タイトル, 商品タイプ, ベンダー, 価格, 在庫)
PRODUCTS = [
    ("Aurora Hoodie", "Apparel", "Northlight", 6800, 40),
    ("Cascade Water Bottle", "Accessories", "Northlight", 2200, 120),
    ("Ember Scented Candle", "Home", "Hearth&Co", 1800, 80),
    ("Nimbus Rain Jacket", "Apparel", "Northlight", 12800, 25),
    ("Pebble Wireless Mouse", "Electronics", "Cobalt", 3900, 60),
    ("Slate Notebook A5", "Stationery", "Cobalt", 900, 200),
]

# 顧客: (姓, 名, メール, 国コード)
CUSTOMERS = [
    ("Yui", "Tanaka", "yui.tanaka@example.com", "JP"),
    ("Ken", "Sato", "ken.sato@example.com", "JP"),
    ("Emma", "Brown", "emma.brown@example.com", "US"),
    ("Liam", "Wilson", "liam.wilson@example.com", "GB"),
]

# 割引: dict でタイプ別に定義。dlt が取得する discounts の多様性を担保する。
#   kind: percentage(定率コード) / amount(定額コード) / free_shipping(送料無料コード) / automatic(自動定率)
DISCOUNTS = [
    {"kind": "percentage", "title": "Spring Sale 10%", "code": "SPRING10", "percentage": 0.10,
     "usage_limit": 100},
    {"kind": "amount", "title": "500 OFF Coupon", "code": "SAVE500", "amount": 500,
     "usage_limit": 50},
    {"kind": "free_shipping", "title": "Free Shipping", "code": "FREESHIP", "usage_limit": 200},
    {"kind": "automatic", "title": "Auto 5% Off", "percentage": 0.05},
]

# 注文: (顧客インデックス, [(商品インデックス, 数量), ...], 手動割引率 or None)
ORDERS = [
    (0, [(0, 1), (2, 2)], None),
    (1, [(1, 3)], 0.10),
    (2, [(3, 1), (4, 1)], None),
    (3, [(5, 5)], 0.05),
    (0, [(4, 2)], None),
    (1, [(2, 1), (5, 3)], 0.10),
    (2, [(0, 1)], None),
    (3, [(1, 2), (3, 1)], None),
]
