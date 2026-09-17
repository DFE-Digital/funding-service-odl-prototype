with values as (select 
    academic_year,
    urn,
    la_estab,
    ukprn,
    la_number,
    la_name,
    provider_name,
    type_of_establishment_name,
    phase_of_education_name,
    -- for proivisional calculations we use
    -- max(AVG(UIFSM ELIGIBLE OVER OCT JAN), UIFSM JAN)
    --Y1,Y2= AVG(UIFSM OCT,JAN)
    -- see notes tab of provisional calculations excel available here https://www.gov.uk/government/publications/universal-infant-free-school-meals-uifsm-2026-to-2027
    greatest((coalesce(total_uifsm_meals_R, 0) + coalesce(total_uifsm_meals_R_jan, 0))/2, total_uifsm_meals_R_jan ) as UIFSM_total_meals_R,


    (coalesce(total_uifsm_meals_1, 0) + coalesce(total_uifsm_meals_1_jan, 0) +
    coalesce(total_uifsm_meals_2, 0) + coalesce(total_uifsm_meals_2_jan, 0) +
    coalesce(total_uifsm_meals_X4, 0) + coalesce(total_uifsm_meals_X4_jan, 0) +
    coalesce(total_uifsm_meals_X5, 0) + coalesce(total_uifsm_meals_X5_jan, 0) +
    coalesce(total_uifsm_meals_X6, 0) + coalesce(total_uifsm_meals_X6_jan, 0)) /2  as UIFSM_total_meals_Y1_Y2,
    -- divided by 2 above as the _X columns still refer to pupils that would usually be in yr1/2 just not following curriculumn

from {{ref('joined_uifsm_meal_takeup_census_2526')}})
select 
 *,
 UIFSM_total_meals_R + UIFSM_total_meals_Y1_Y2 as UIFSM_total_eligible_meals
 from values