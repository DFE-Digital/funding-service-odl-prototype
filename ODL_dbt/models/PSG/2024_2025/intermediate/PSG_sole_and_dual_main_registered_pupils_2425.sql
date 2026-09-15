--sole and dual main registered pupils census datasets have the exact same ukprns in - we need the total of the 
--sole and dual registered pupils for each ukprn to get the total number of pupils in each school eligible for PSG funding
WITH joined as (

SELECT 
    sr.academic_year,
  sr.census_term,
  sr.urn,
  sr.ukprn,
  sr.la_number,
  sr.la_name,
  sr.la_estab,
  sr.provider_name,
  sr.type_of_establishment_name,
  sr.phase_of_education_name,
  sr.NCY_R + dr.NCY_R as NCY_R,
  sr.NCY_1 + dr.NCY_1 as NCY_1,
  sr.NCY_2 + dr.NCY_2 as NCY_2,
  sr.NCY_3 + dr.NCY_3 as NCY_3,
  sr.NCY_4 + dr.NCY_4 as NCY_4,
  sr.NCY_5 + dr.NCY_5 as NCY_5,
  sr.NCY_6 + dr.NCY_6 as NCY_6, 
  sr.NCY_7 + dr.NCY_7 as NCY_7,
    sr.NCY_X5to10 + dr.NCY_X5to10 as NCY_X5to10
FROM {{ref('PSG_sole_main_registered_pupils_census_2425')}} sr
INNER JOIN {{ref('PSG_dual_main_registered_pupils_census_2425')}} dr ON sr.ukprn = dr.ukprn
) select * from joined