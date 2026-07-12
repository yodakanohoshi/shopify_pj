# raw.collection_products

コレクション所属商品のブリッジ。取得方式: **Bulk** (`collections.products`)。
粒度: 1 行 = (コレクション × 商品)。

| 日本語名 | 論理名 | 型 | 説明 |
|---|---|---|---|
| 商品ID | id | varchar | 商品 gid。**FK → products.id** |
| 親ID | parent_id | varchar | コレクション gid。**FK → collections.id** |

> id は複数コレクションに跨って重複しうる (同一商品が複数コレクションに所属)。
