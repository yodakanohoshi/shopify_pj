"""取得対象エンドポイントの宣言的な定義。

`dataload/` の Shopify 版が ``queries.py`` に GraphQL を並べるのと同じ位置づけで、
REST 版はここに「どのパスを、どうページングし、どう差分取得するか」を並べる。
対象 API に合わせて書き換えるのは基本的にこのファイルだけで済むようにしている。

差分取得の考え方 (Shopify 版と同一):

- ``cursor_field`` … レコード内の更新時刻フィールド。取得したレコードの最大値を
  高水位としてパイプライン状態に保存する (前進のみ)。
- ``filter_param`` … 高水位を API 側の絞り込みに渡すクエリパラメータ名
  (``updated_since`` / ``updated_at_min`` など API により異なる)。
- ``end_param`` … 期間指定バックフィルの上限を渡すパラメータ名 (無ければ ``None``)。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Endpoint:
    """1つの REST エンドポイント = 1つの dlt リソース。"""

    name: str  # dlt リソース名 = 出力テーブル名
    path: str  # base_url からの相対パス (例 "orders")
    data_path: str | None = "data"  # 応答中のレコード配列の位置。None ならトップレベルが配列
    primary_key: str = "id"

    # --- ページング -------------------------------------------------------
    style: str = "page"  # page / offset / cursor / link
    page_param: str = "page"
    size_param: str = "per_page"
    offset_param: str = "offset"
    cursor_param: str = "cursor"
    cursor_path: str = "next_cursor"  # 応答ボディ中の次カーソルの位置
    start_page: int = 1

    # --- 差分取得 ---------------------------------------------------------
    # incremental=False のエンドポイントは毎回全件取得し replace で洗い替える
    # (件数が少なく変動の小さいディメンション向け)。
    incremental: bool = True
    cursor_field: str = "updated_at"  # レコード側の更新時刻フィールド
    filter_param: str = "updated_since"  # 高水位を渡すクエリパラメータ
    end_param: str | None = None  # 期間バックフィルの上限パラメータ (無ければ None)
    params: dict[str, Any] = field(default_factory=dict)  # 常に付与する固定パラメータ

    @property
    def write_disposition(self) -> str:
        return "merge" if self.incremental else "replace"


# 取得対象。対象 API に合わせてここを書き換える。
# 下記は「``{"data": [...], "meta": {...}}`` を返し、``updated_since`` で絞れる
# ページ番号ページングの API」という一般的な形を仮定したサンプル定義。
ENDPOINTS: list[Endpoint] = [
    Endpoint(
        name="orders",
        path="orders",
        style="page",
        cursor_field="updated_at",
        filter_param="updated_since",
        end_param="updated_until",
    ),
    Endpoint(
        name="customers",
        path="customers",
        style="page",
        cursor_field="updated_at",
        filter_param="updated_since",
        end_param="updated_until",
    ),
    Endpoint(
        name="products",
        path="products",
        style="page",
        cursor_field="updated_at",
        filter_param="updated_since",
        end_param="updated_until",
    ),
    # 小さなディメンションは差分に載せず毎回全件洗い替え (Shopify 版の locations と同じ扱い)
    Endpoint(name="categories", path="categories", incremental=False),
]
