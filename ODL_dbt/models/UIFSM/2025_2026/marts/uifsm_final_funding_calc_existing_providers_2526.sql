
with intermediate_data as (
    select * from {{ ref('max_values_uifsm_eligible_meal_takeup_2526') }}
),
-- final funding calc for 2025-2026 as whole year, 190 school days 2.61 per meal
-- see https://www.gov.uk/government/publications/universal-infant-free-school-meals-uifsm-2025-to-2026/universal-infant-free-school-meals-uifsm-conditions-of-grant-2025-to-2026
calculated as (
    select
        *,
        
        ceil({{ UIFSM('(UIFSM_total_eligible_meals)','(12/12)','190','2.61') }}) as final_UIFSM_funding

    from intermediate_data
)

select * from calculated
order by la_number, la_estab