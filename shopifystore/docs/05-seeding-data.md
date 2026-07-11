# 05. 初期データ投入 (seed)

開発ストアに、分析基盤の検証に足るデータを Admin API 経由で投入する。

## 投入されるもの

| カテゴリ | 件数 | 分析での狙い |
|---|---|---|
| 商品 (原価付き) | 8 | 売上・**粗利** (price − cost) |
| 顧客 (配信同意あり/なし) | 5 | **セグメント**・配信可能率 |
| コレクション | 3 | **カテゴリ**別分析 |
| 割引 (定率/定額/送料無料/自動) | 4 | **販促効果** |
| 注文 (一部に手動割引) | 10 | 売上・割引・チャネル |

データ定義は [`../seed/sample_data.py`](../seed/sample_data.py)。自由に増やしてよい。

## 実行

```powershell
cd shopifystore\seed
uv sync
Copy-Item .env.example .env   # SHOPIFY_SHOP / SHOPIFY_CLIENT_ID / SHOPIFY_CLIENT_SECRET を記入

# 全カテゴリ投入 (products → customers → collections → discounts → orders の順)
uv run python seed.py

# 一部だけ投入
uv run python seed.py --only products,collections
```

## 仕組み (何をしているか)

| カテゴリ | 使う GraphQL mutation |
|---|---|
| 商品 | `productCreate` → `productVariantsBulkUpdate` (price + inventoryItem.cost) |
| 顧客 | `customerCreate` → `customerEmailMarketingConsentUpdate` |
| コレクション | `collectionCreate` → `collectionAddProducts` |
| 割引 | `discountCodeBasicCreate` / `discountCodeFreeShippingCreate` / `discountAutomaticBasicCreate` |
| 注文 | `draftOrderCreate` → `draftOrderComplete` (paymentPending) |

- 注文は**ドラフト注文を確定**して作る (実決済なし)。
- 各 mutation は `userErrors` を検査し、失敗時は原因を表示して停止する。

## 注意

- **書き込みスコープ**が必要 (`write_products` 等)。[02](02-dev-store-and-app.md) 参照。
- 顧客・注文には **保護対象顧客データアクセス (Level 2)** が必要。[02 ステップ3.5](02-dev-store-and-app.md) 参照。
- 放棄チェックアウトは API で直接作れない (実際のカゴ落ちで発生)。seed 対象外。

## 再実行時の挙動 (冪等性)

- **商品 (title) / 顧客 (email) / コレクション (title) / 割引 (code)** は、既存があれば
  **再利用またはスキップ**する。よって seed の再実行は安全。
- **注文**のみ自然キーが無いため、再実行すると**追加で作成**される (重複)。
  注文を増やしたくない場合は `--only products,customers,collections,discounts` を使う。
- 以前の失敗実行で**重複商品**などが残っている場合、クリーンにしたいときは
  ストア管理画面から削除するか、新しい開発ストアで実行する。

投入後は [04. 分析基盤の動かし方](04-analytics-system.md) に戻ってパイプラインを回す。
