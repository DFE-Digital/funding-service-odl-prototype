{% macro sum_columns(columns) %}
    -- takes a list of column names and returns a SQL expression that sums them, treating nulls as zero
    {% set safe_cols = [] %}
    {% for col in columns %}
        {% do safe_cols.append('coalesce(' ~ col ~ ', 0)') %}
    {% endfor %}
    ({{ safe_cols | join(' + ') }})
{% endmacro %}
