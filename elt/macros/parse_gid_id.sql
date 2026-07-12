{#
  parse_gid_id: Shopify の global ID から ID 部分を文字列で取り出す。

  例: 'gid://shopify/Order/12345'                          -> '12345'
      'gid://shopify/InventoryLevel/12?inventory_item_id=34' -> '12'  (クエリ文字列は除去)

  '?' 以降を落としてから末尾の連続文字を抽出する。**数値化はせず varchar のまま**
  (ID は文字列として扱う)。null はそのまま null。

  結合キー (PK と、それを参照する FK) の双方に同じマクロを適用すること。
  でないと gid と抽出後 ID が混在して結合が壊れる。
#}
{% macro parse_gid_id(column) %}
    regexp_extract(split_part({{ column }}, '?', 1), '[0-9]+$')
{%- endmacro %}
