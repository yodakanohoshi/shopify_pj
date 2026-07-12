{#
  raw_source: スパースな raw ソースに追従するための堅牢化マクロ。

  dlt はデータ駆動でスキーマを作るため、全行 NULL のカラムや 0 件のテーブルは
  生成されない。その結果、フルスキーマ前提の staging モデルが実データ (特に seed の
  疎なデータ) で「column not found」「table does not exist」で落ちる。

  このマクロは staging モデルの source CTE を置き換え、次を保証する:
  - ソーステーブルが存在する場合: `select *` に加え、`expected_columns` のうち
    実在しないものを `cast(null as varchar) as <col>` で補完する。
  - ソーステーブル自体が存在しない場合: `expected_columns` を NULL 列として持つ
    0 行の結果を返す (下流はそのまま 0 行で通る)。

  NULL 補完は varchar 固定。staging 側の明示 cast (timestamp/integer/double 等) が
  そのまま効くため、型は問題にならない。

  使い方:
    with source as (
        {{ raw_source(source('shopify_raw', 'orders'), [
            'id', 'name', 'po_number', 'created_at', ...  -- モデルが参照する raw カラム
        ]) }}
    )
    select ... from source
#}
{% macro raw_source(relation, expected_columns) %}
{%- if not execute -%}
    select * from {{ relation }}
{%- else -%}
    {%- set rel = adapter.get_relation(database=relation.database, schema=relation.schema, identifier=relation.identifier) -%}
    {%- if rel is none -%}
        select
        {%- for c in expected_columns %}
            cast(null as varchar) as {{ c }}{{ "," if not loop.last }}
        {%- endfor %}
        limit 0
    {%- else -%}
        {%- set existing = adapter.get_columns_in_relation(rel) | map(attribute='name') | map('lower') | list -%}
        select *
        {%- for c in expected_columns if (c | lower) not in existing %}
        , cast(null as varchar) as {{ c }}
        {%- endfor %}
        from {{ relation }}
    {%- endif -%}
{%- endif -%}
{% endmacro %}
