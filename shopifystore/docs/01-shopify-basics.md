# 01. Shopify の基礎と用語

Shopify を初めて触る人向けに、分析基盤を理解するのに必要な最低限の用語を整理する。

## Shopify とは

Shopify は EC ストアを構築・運営する SaaS。商品登録・注文・顧客・割引・在庫などを
管理画面 (Admin) で扱い、それらのデータは **Admin API** で外部から取得できる。
本プロジェクトはこの API を通じてデータを取り出し、分析用に整える。

## 押さえるべき登場人物

| 用語 | 説明 |
|---|---|
| **Dev Dashboard** | Shopify 開発の統合ハブ（<https://dev.shopify.com/dashboard>）。アプリ・ストアを一元管理。本プロジェクトの入口 |
| **Shopify Partner** | 開発者向けの無料アカウント。Dev Dashboard へは Partner からも入れる |
| **開発ストア (dev store)** | テスト用の無料ストア。本番販売はできないが機能はほぼ同じ。分析検証に最適 |
| **Admin (管理画面)** | ストアの運営画面。商品・注文・割引などをここで操作する |
| **アプリ (app)** | **Admin API トークン**を発行する入口。Dev Dashboard で作成しストアにインストールする |
| **Admin API** | ストアデータを読み書きする API。本プロジェクトは **GraphQL** 版を使う |
| **アクセススコープ (scope)** | API で何を読めるかの権限 (例: `read_orders`, `read_discounts`) |
| **Shopify CLI** | テーマ/アプリ開発用のコマンドラインツール (分析基盤には必須ではない) |

## データの流れ (全体像)

```
[あなたの開発ストア]
      │  Admin GraphQL API (トークンで認証)
      ▼
  dataload/  … dlt がデータを取り出し DuckDB の raw へ
      ▼
  elt/       … dbt が raw を分析用テーブル (marts) へ変換
      ▼
  分析 / BI  … marts を SQL や BI ツールで参照
```

## GraphQL と REST

Shopify は現在 **GraphQL Admin API を推奨**しており、REST の一部エンドポイントは
廃止が進んでいる。本プロジェクトは GraphQL に統一している (大量データは **Bulk Operations**)。

## global ID (gid)

GraphQL のオブジェクト ID は `gid://shopify/Order/123456` の形式 (global ID)。
数値だけの旧 ID は `legacyResourceId` として別途取得できる。分析では gid を主キーに使う。

次は [02. 開発ストアとカスタムアプリの作成](02-dev-store-and-app.md)。
