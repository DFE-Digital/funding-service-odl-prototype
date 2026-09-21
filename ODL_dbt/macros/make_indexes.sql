{% macro add_key(key_columns) %}

    
    {% set columns = key_columns %}

    {% do log("columns=" ~ columns, info=True) %}

    {% set col_list = columns | join(', ') %}
    {% set key_name = 'pk_' ~ this.identifier %}

    {% if target.type == 'duckdb' %}
        {% set sql %}
            create index if not exists {{ key_name }}
            on {{ this }} ({{ col_list }})
        {% endset %}
    {% elif target.type in ['mysql', 'dolt'] %}
        {% set sql %}
            alter table {{ this }}
            add primary key ({{ col_list }})
        {% endset %}
    {% endif %}

    {{ return(sql) }}

{% endmacro %}