--staging sole and dual ghs registered pupils have exactly same estabs in  - we need the total of the 
--sole and dual registered pupils for each estab to get the total number of pupils in each ghs eligible for PSG funding
WITH joined as (

SELECT 
    sr.urn,
    sr.ukprn,
    sr.la_number,
    sr.la_name,
    sr.laestab,
    sr.provider_name,
    sr.type_of_establishment_name,
    sr.phase_of_education_name,
    sr.Age5_Total + dr.Age5_Total as Age5_Total,
    sr.Age6_Total + dr.Age6_Total as Age6_Total,
    sr.Age7_Total + dr.Age7_Total as Age7_Total,
    sr.Age8_Total + dr.Age8_Total as Age8_Total,
    sr.Age9_Total + dr.Age9_Total as Age9_Total,
    sr.Age10_Total + dr.Age10_Total as Age10_Total
FROM {{ref('PSG_sole_registered_GHS_census_2526')}} sr
INNER JOIN {{ref('PSG_dual_registered_GHS_census_2526')}} dr ON sr.laestab = dr.laestab
) select * from joined