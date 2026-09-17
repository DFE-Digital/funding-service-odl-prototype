
with intermediate_data as (
    select * from {{ ref('max_values_uifsm_eligible_meal_takeup_2122') }}
),
-- initial funding calc for 2022-2023 as 7/12 of the year, 190 school days 2.41 per meal
-- see https://www.gov.uk/government/publications/universal-infant-free-school-meals-uifsm-2022-to-2023/universal-infant-free-school-meals-uifsm-conditions-of-grant-2022-to-2023
calculated as (
    select
        *,
        ceil({{ UIFSM('(UIFSM_total_eligible_meals)','(7/12)','190','2.41') }}) as provisional_UIFSM_funding

    from intermediate_data
)

select * from calculated
order by la_number, urn