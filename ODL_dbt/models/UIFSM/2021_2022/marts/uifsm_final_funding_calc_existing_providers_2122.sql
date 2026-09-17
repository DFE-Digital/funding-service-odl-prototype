
with intermediate_data as (
    select * from {{ ref('max_values_uifsm_eligible_meal_takeup_2122') }}
),
-- final funding calc for 2021-2022 as whole year, 190 school days 2.34 per meal
-- see https://www.gov.uk/government/publications/universal-infant-free-school-meals-uifsm-2021-to-2022/universal-infant-free-school-meals-uifsm-conditions-of-grant-2021-to-2022
calculated as (
    select
        *,
        
        ceil({{ UIFSM('(UIFSM_total_eligible_meals)','(12/12)','190','2.34') }}) as final_UIFSM_funding

    from intermediate_data
)

select * from calculated
order by la_number, urn