# shopifystore/docs — はじめての Shopify + 分析基盤ガイド

Shopify を初めて使う人向けに、開発ストアの用意から分析基盤が動くまでを順に解説する。

| # | ドキュメント | 内容 |
|---|---|---|
| 01 | [Shopify の基礎と用語](01-shopify-basics.md) | Shopify とは / Partner / 開発ストア / アプリ / Admin API の全体像 |
| 02 | [開発ストアとカスタムアプリの作成](02-dev-store-and-app.md) | Partner 登録 → 開発ストア → カスタムアプリ → API トークン取得 |
| 03 | [Shopify のデータモデル](03-data-model.md) | 注文・商品・顧客・割引・コレクション等の関係 (分析の対象) |
| 04 | [分析基盤の仕組みと動かし方](04-analytics-system.md) | dlt → dbt → DuckDB のパイプライン全体と実行手順 |
| 05 | [初期データ投入 (seed)](05-seeding-data.md) | seed スクリプトで投入されるデータと使い方 |

まず 01 → 02 で「動くストアとトークン」を用意し、05 でデータを入れ、04 でパイプラインを回す。
