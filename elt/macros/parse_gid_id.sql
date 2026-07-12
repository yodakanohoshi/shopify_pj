{#
  parse_gid_id: Shopify の global ID から数値 ID を取り出す。

  例: 'gid://shopify/Order/12345'                      -> 12345
      'gid://shopify/InventoryLevel/12?inventory_item_id=34' -> 12  (クエリ文字列は除去)

  '?' 以降を落としてから末尾の連続数字を抽出し bigint にする。null はそのまま null。
  数値化できない gid (例: TaxonomyCategory の 'aa-1-2') には使わないこと。

  結合キー (PK と、それを参照する FK) の双方に同じマクロを適用すること。
  でないと gid と数値が混在して結合が壊れる。
#}
{% macro parse_gid_id(column) %}
    try_cast(regexp_extract(split_part({{ column }}, '?', 1), '[0-9]+$') as bigint)
{%- endmacro %}
