{#
  カスタムスキーマ名をそのまま採用する (既定の <target>_<custom> 連結をしない)。
  これにより staging / intermediate / marts が独立スキーマとして出力される。
#}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
