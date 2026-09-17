
with intermediate_data as (
    select * from {{ ref('max_values_uifsm_eligible_meal_takeup_2526') }}
),
-- initial funding calc for 2026-2027 as 7/12 of the year, 190 school days 2.66 per meal
-- see https://www.gov.uk/government/publications/universal-infant-free-school-meals-uifsm-2026-to-2027/universal-infant-free-school-meals-uifsm-conditions-of-grant-2026-to-2027
calculated as (
    select
        *,
        -- funding * 0.8 to avoid over funding as per https://www.gov.uk/government/publications/universal-infant-free-school-meals-uifsm-2026-to-2027/universal-infant-free-school-meals-uifsm-conditions-of-grant-2026-to-2027
        ceil((0.8 * {{ UIFSM('(UIFSM_total_eligible_meals)','(7/12)','190','2.66') }})) as provisional_UIFSM_funding

    from intermediate_data
)

select * from calculated
order by la_number, la_estab