"""ページングのある一般的な REST API を対象とした dlt ソース。

`dataload/` の Shopify ソースと同じ構造・同じ運用モードを、GraphQL/Bulk ではなく
**通常の REST + ページング** で実現する。認証フロー (Client Credentials Grant /
静的トークン) と取得モード (差分 / バックフィル) は Shopify 版と同一。

## 取得モード

- **差分取得 (既定)**: 日次/毎時のスケジュール実行。前回実行で記録した高水位
  (``updated_at`` 等) 以降だけを API 側のクエリパラメータ (``updated_since`` 等) で
  絞って取得し、``merge`` で upsert する。初回実行は高水位が無いため自動的に
  全件取得 (= 初回バックフィル) となる。
- **バックフィル (手動・随時)**: ``backfill=True`` または ``start_date`` / ``end_date``
  で期間を指定して呼ぶ。保存済み高水位を無視して対象期間を再取得する。
  高水位は前進のみ (過去窓の再取得で巻き戻さない)。

大きく変動しない小さなディメンション (``incremental=False`` のエンドポイント) は
差分に載せず、毎回 ``replace`` で全件洗い替えする。

取得対象の追加・変更は `endpoints.py` の ``ENDPOINTS`` を編集するだけでよい。
"""

from __future__ import annotations

from typing import Any, Iterable, Iterator

import dlt
from dlt.sources import DltResource

from .endpoints import ENDPOINTS, Endpoint
from .helpers import RestClient, paginate


@dlt.source(name="rest_api")
def rest_api_source(
    base_url: str = dlt.config.value,
    access_token: str | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
    token_url: str | None = None,
    scope: str | None = None,
    auth_scheme: str = "Bearer",
    page_size: int = 100,
    start_date: str | None = None,
    end_date: str | None = None,
    backfill: bool = False,
) -> Iterable[DltResource]:
    """REST API の各エンドポイントを raw スキーマへロードするソース。

    認証は client_id + client_secret (Client Credentials Grant) か access_token の
    いずれか。dlt が config/secrets/環境変数から注入する。

    差分取得とバックフィルの切り替え:

    - 既定 (``start_date`` / ``end_date`` を渡さず ``backfill=False``): 差分取得。
      各リソースは前回の高水位以降のみを取得し ``merge`` で upsert する。
    - ``backfill=True``: 保存済み高水位を無視して全期間を再取得する。
    - ``start_date`` / ``end_date`` (ISO8601 例 ``"2025-01-01"``): 期間を指定した
      バックフィル。片方だけでも可 (下限のみ / 上限のみ)。

    ``start_date`` を渡した場合は ``backfill`` 指定に関わらずバックフィル扱いとなる。
    """

    client = RestClient(
        base_url=base_url,
        access_token=access_token,
        client_id=client_id,
        client_secret=client_secret,
        token_url=token_url,
        scope=scope,
        auth_scheme=auth_scheme,
    )

    # start_date 明示 or backfill フラグ → バックフィル (保存済み高水位を無視)
    manual = backfill or start_date is not None

    def _resource(endpoint: Endpoint) -> DltResource:
        """1つのエンドポイントを、差分/バックフィルどちらでも動く形で生成する。"""

        @dlt.resource(
            name=endpoint.name,
            primary_key=endpoint.primary_key,
            write_disposition=endpoint.write_disposition,
        )
        def resource() -> Iterator[dict[str, Any]]:
            params = dict(endpoint.params)
            state = dlt.current.resource_state() if endpoint.incremental else {}
            cursor = state.get("cursor")  # 高水位は前進のみ (max)

            if endpoint.incremental:
                # 差分取得: 保存済み高水位を下限に。バックフィル: start_date を下限に (None=全件)。
                low = start_date if manual else cursor
                if low:
                    params[endpoint.filter_param] = low
                if end_date and endpoint.end_param:
                    params[endpoint.end_param] = end_date

            for record in paginate(
                client,
                endpoint.path,
                data_path=endpoint.data_path,
                params=params,
                style=endpoint.style,
                page_size=page_size,
                page_param=endpoint.page_param,
                size_param=endpoint.size_param,
                offset_param=endpoint.offset_param,
                cursor_param=endpoint.cursor_param,
                cursor_path=endpoint.cursor_path,
                start_page=endpoint.start_page,
            ):
                if endpoint.incremental:
                    value = record.get(endpoint.cursor_field)
                    if value and (cursor is None or value > cursor):
                        cursor = value
                yield record

            if endpoint.incremental and cursor is not None:
                state["cursor"] = cursor

        return resource

    return [_resource(endpoint) for endpoint in ENDPOINTS]
