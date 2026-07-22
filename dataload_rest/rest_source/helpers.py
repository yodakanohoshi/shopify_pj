"""汎用 REST API クライアントとページングヘルパー。

認証は `dataload/` の Shopify 版と同じ2方式に対応する:

- **Client Credentials Grant** (推奨): token エンドポイントに client_id / client_secret を
  送ってアクセストークンを取得する (期限付きのため自動更新)。
- **静的トークン**: 発行済みの固定トークンをそのまま Authorization ヘッダに載せる。

ページングは REST API ごとに流儀が異なるため、代表的な4方式を実装する:

- ``page``   : ``?page=1&per_page=100`` 形式のページ番号
- ``offset`` : ``?offset=0&limit=100`` 形式のオフセット
- ``cursor`` : 応答ボディ中の次カーソル (``next_cursor`` 等) を次リクエストへ渡す
- ``link``   : ``Link: <...>; rel="next"`` ヘッダ (GitHub / Shopify REST 系)
"""

from __future__ import annotations

import re
import time
from typing import Any, Iterator

import requests

_MAX_RETRIES = 6  # 429 / 5xx に対するリトライ回数
_TOKEN_MARGIN = 60  # トークン失効の何秒前に更新するか
_MAX_BACKOFF = 30  # 指数バックオフの上限秒
_LINK_NEXT = re.compile(r'<([^>]+)>\s*;\s*rel="?next"?')


class RestAPIError(RuntimeError):
    """REST API 呼び出しの失敗をまとめて送出する。"""


class RestClient:
    """REST API への薄いクライアント。

    - Client Credentials Grant / 静的トークンの両対応 (Authorization ヘッダ)
    - 429 / 5xx に対する ``Retry-After`` 尊重 + 指数バックオフ
    - ``X-RateLimit-Remaining`` が枯渇しかけていれば ``X-RateLimit-Reset`` まで待つ
    """

    def __init__(
        self,
        base_url: str,
        access_token: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        token_url: str | None = None,
        scope: str | None = None,
        auth_header: str = "Authorization",
        auth_scheme: str = "Bearer",
        timeout: int = 60,
    ):
        # 末尾スラッシュの有無を吸収し、パス結合時の "//" を防ぐ
        self.base_url = base_url.rstrip("/")
        self._token_url = token_url or f"{self.base_url}/oauth/token"
        self._scope = scope or None

        self._static_token = access_token or None
        self._client_id = client_id or None
        self._client_secret = client_secret or None
        if not self._static_token and not (self._client_id and self._client_secret):
            raise RestAPIError(
                "認証情報が未設定です。access_token、または client_id + client_secret を設定してください。"
            )

        self._auth_header = auth_header
        self._auth_scheme = auth_scheme
        self._session = requests.Session()
        self._session.headers.update({"Accept": "application/json"})
        self._timeout = timeout
        self._token: str | None = None
        self._token_expiry = 0.0

    # --- 認証 -------------------------------------------------------------
    def _access_token(self) -> str:
        if self._static_token:
            return self._static_token
        if self._token and time.monotonic() < self._token_expiry:
            return self._token
        payload = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }
        if self._scope:
            payload["scope"] = self._scope
        resp = requests.post(self._token_url, data=payload, timeout=30)
        if resp.status_code >= 400:
            raise RestAPIError(
                f"アクセストークン取得に失敗 (HTTP {resp.status_code})。"
                f"token_url と Client ID/Secret を確認してください。\n"
                f"  URL: {self._token_url}\n  応答: {resp.text[:400]}"
            )
        data = resp.json()
        if "access_token" not in data:
            raise RestAPIError(f"token 応答に access_token がありません: {str(data)[:400]}")
        self._token = data["access_token"]
        # expires_in 未返却の API もあるため既定1時間として扱う
        self._token_expiry = time.monotonic() + float(data.get("expires_in", 3600)) - _TOKEN_MARGIN
        return self._token

    # --- 実行 -------------------------------------------------------------
    def get(self, url: str, params: dict[str, Any] | None = None) -> requests.Response:
        """GET を1回実行する (相対パスなら base_url を前置)。レート制限は自動で待つ。"""
        if not url.startswith("http"):
            url = f"{self.base_url}/{url.lstrip('/')}"
        # None の値はクエリ文字列に載せない (API 側で空文字と解釈されるのを避ける)
        query = {k: v for k, v in (params or {}).items() if v is not None}

        for attempt in range(_MAX_RETRIES):
            token = self._access_token()
            header = f"{self._auth_scheme} {token}".strip() if self._auth_scheme else token
            self._session.headers[self._auth_header] = header
            resp = self._session.get(url, params=query, timeout=self._timeout)

            if resp.status_code in (429, 500, 502, 503, 504):
                self._sleep_backoff(attempt, resp)
                continue

            if resp.status_code >= 400:
                hint = ""
                if resp.status_code == 401:
                    hint = " — トークンが無効か失効しています"
                elif resp.status_code == 403:
                    hint = " — スコープ (権限) 不足です"
                elif resp.status_code == 404:
                    hint = " — エンドポイントのパスを確認してください"
                raise RestAPIError(
                    f"HTTP {resp.status_code}{hint}\n  URL: {resp.url}\n  応答: {resp.text[:500]}"
                )

            self._respect_rate_limit(resp)
            return resp

        raise RestAPIError(f"リトライ上限 ({_MAX_RETRIES}) 到達: {url}")

    # --- レート制御 -------------------------------------------------------
    @staticmethod
    def _sleep_backoff(attempt: int, resp: requests.Response) -> None:
        retry_after = resp.headers.get("Retry-After")
        try:
            wait = float(retry_after) if retry_after else min(2**attempt, _MAX_BACKOFF)
        except ValueError:  # HTTP-date 形式の Retry-After は解釈せず既定待ちにする
            wait = min(2**attempt, _MAX_BACKOFF)
        time.sleep(wait)

    @staticmethod
    def _respect_rate_limit(resp: requests.Response) -> None:
        """残枠が尽きかけていれば、次リクエスト前に軽く待つ (ヘッダがある API のみ)。"""
        remaining = resp.headers.get("X-RateLimit-Remaining") or resp.headers.get(
            "RateLimit-Remaining"
        )
        reset = resp.headers.get("X-RateLimit-Reset") or resp.headers.get("RateLimit-Reset")
        if remaining is None:
            return
        try:
            if int(float(remaining)) > 0:
                return
            wait = float(reset) if reset else 1.0
        except ValueError:
            return
        # Reset は「残り秒数」と「epoch 秒」の2流儀がある。大きすぎる値は epoch とみなす。
        if wait > 1e6:
            wait -= time.time()
        time.sleep(max(min(wait, _MAX_BACKOFF), 0))


def paginate(
    client: RestClient,
    path: str,
    data_path: str | None = None,
    params: dict[str, Any] | None = None,
    style: str = "page",
    page_size: int = 100,
    page_param: str = "page",
    size_param: str = "per_page",
    offset_param: str = "offset",
    cursor_param: str = "cursor",
    cursor_path: str = "next_cursor",
    start_page: int = 1,
) -> Iterator[dict[str, Any]]:
    """REST エンドポイントをページングし、レコードを1件ずつ yield する。

    ``style`` で流儀を切り替える (``page`` / ``offset`` / ``cursor`` / ``link``)。
    ``data_path`` は応答ボディ中のレコード配列の位置 (``"data"``、``"result.items"`` 等)。
    ``None`` ならトップレベルが配列であることを期待する。
    """
    base_params = dict(params or {})
    page = start_page
    offset = 0
    cursor: str | None = None
    url: str | None = path
    seen_pages = 0

    while True:
        query = dict(base_params)
        if style == "page":
            query[page_param] = page
            query[size_param] = page_size
        elif style == "offset":
            query[offset_param] = offset
            query[size_param] = page_size
        elif style == "cursor":
            query[size_param] = page_size
            if cursor:
                query[cursor_param] = cursor
        elif style == "link":
            query[size_param] = page_size
        else:
            raise RestAPIError(f"未知のページング方式: {style}")

        # link 方式の2ページ目以降は next URL がクエリを内包するため params を渡さない
        follow_url = url if style == "link" and seen_pages else path
        resp = client.get(follow_url, None if (style == "link" and seen_pages) else query)
        body = resp.json()
        records = _extract(body, data_path)
        if not isinstance(records, list):
            raise RestAPIError(
                f"data_path='{data_path}' がリストを指していません: {type(records).__name__}"
            )

        yield from records
        seen_pages += 1

        if style == "link":
            url = _next_link(resp)
            if not url:
                break
        elif style == "cursor":
            cursor = _extract(body, cursor_path)
            if not cursor:
                break
        else:
            # ページ番号/オフセット方式は、満たないページ = 最終ページとみなす
            if len(records) < page_size:
                break
            page += 1
            offset += page_size


def _extract(body: Any, path: str | None) -> Any:
    """``"result.items"`` のようなドット区切りパスでネストした値を取り出す。"""
    if path is None:
        return body
    value: Any = body
    for key in path.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def _next_link(resp: requests.Response) -> str | None:
    """``Link`` ヘッダから ``rel="next"`` の URL を取り出す。"""
    link = resp.headers.get("Link") or resp.headers.get("link")
    if not link:
        return None
    match = _LINK_NEXT.search(link)
    return match.group(1) if match else None
