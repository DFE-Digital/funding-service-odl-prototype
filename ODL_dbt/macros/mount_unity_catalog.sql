{% macro mount_unity_catalog() %}
    {% set mount_query %}
        INSTALL delta; LOAD delta;
        INSTALL unity_catalog; LOAD unity_catalog;
       CREATE SECRET IF NOT EXISTS (
            TYPE UNITY_CATALOG, 
            TOKEN '{{ env_var("DATABRICKS_ACCESS_TOKEN") }}', 
            ENDPOINT '{{ env_var("DATABRICKS_SERVER_HOSTNAME") }}/'
        );
        ATTACH IF NOT EXISTS 'catalog_30_bronze' AS catalog_30_bronze (TYPE UNITY_CATALOG);
    {% endset %}

    {% do run_query(mount_query) %}
    {% do log("Successfully attached Unity Catalog via startup macro", info=True) %}
{% endmacro %}