{% macro UIFSM(UIFSM_pupils, portion_of_fuding_year, school_days_per_year, funding_amount_per_pupil) %}
    -- Calculates UIFSM funding based on the number of UIFAM pupils, the portion of the funding year(prelimiary or residual calculation),
    -- the number of funded school days per year, and the funding amount per eligible pupil
    ({{UIFSM_pupils}}) * {{ portion_of_fuding_year }} * {{ school_days_per_year }} * {{ funding_amount_per_pupil }}
{% endmacro %}

