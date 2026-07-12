"""requests で Shopify API を直接叩き、数件だけ取得して生 JSON を確認する。

Bulk を使わず 1 リクエストで ``first: N`` 件を取り、``samples/<name>.json`` に
整形保存 + キー概要を標準出力する。dbt には流さない、純粋な「どんなデータか」の調査用。

使い方::

    # 全プローブを 3 件ずつ
    uv run python raw_probe.py

    # 特定リソースだけ / 件数指定
    uv run python raw_probe.py --only products customers -n 5
    uv run python raw_probe.py --list

出力の samples/ は .gitignore 済み (生データを誤ってコミットしないため)。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from queries import PROBES
from shopify_client import client_from_env

SAMPLES_DIR = Path(__file__).parent / "samples"


def _unwrap(value: Any) -> Any:
    """``{edges:[{node:{...}}]}`` を素直なリストへ畳んで読みやすくする。"""
    if isinstance(value, dict):
        if "edges" in value and isinstance(value["edges"], list):
            return [_unwrap(e.get("node", e)) for e in value["edges"]]
        return {k: _unwrap(v) for k, v in value.items() if k != "pageInfo"}
    if isinstance(value, list):
        return [_unwrap(v) for v in value]
    return value


def _summfrom(nodes: list[Any]) -> str:
    if not nodes:
        return "  (0 件)"
    keys = sorted(nodes[0].keys()) if isinstance(nodes[0], dict) else []
    return f"  {len(nodes)} 件 / トップレベルキー: {', '.join(keys)}"


def probe(name: str, n: int) -> None:
    root_field, query = PROBES[name]
    client = client_from_env()
    data = client.execute(query, {"n": n})
    nodes = _unwrap(data[root_field])

    SAMPLES_DIR.mkdir(exist_ok=True)
    out = SAMPLES_DIR / f"{name}.json"
    out.write_text(json.dumps(nodes, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[{name}] -> {out.relative_to(Path(__file__).parent)}")
    print(_summfrom(nodes))


def main() -> None:
    parser = argparse.ArgumentParser(description="Shopify API を数件だけ叩いて生 JSON を確認する")
    parser.add_argument("--only", nargs="*", metavar="NAME", help="対象プローブ (既定: 全部)")
    parser.add_argument("-n", type=int, default=3, help="取得件数 (既定 3)")
    parser.add_argument("--list", action="store_true", help="利用可能なプローブ名を表示")
    args = parser.parse_args()

    if args.list:
        print("利用可能なプローブ:")
        for name, (root, _) in PROBES.items():
            print(f"  - {name} (root: {root})")
        return

    targets = args.only or list(PROBES)
    unknown = [t for t in targets if t not in PROBES]
    if unknown:
        raise SystemExit(f"未知のプローブ: {unknown}。--list で一覧を確認してください。")

    for name in targets:
        probe(name, args.n)


if __name__ == "__main__":
    main()
