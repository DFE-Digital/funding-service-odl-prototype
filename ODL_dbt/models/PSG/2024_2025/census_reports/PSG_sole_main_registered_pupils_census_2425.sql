select 
  c.academic_year,
  c.census_term,
  sp.urn,
  sp.ukprn,
  sp.la_number,
  sp.la_name,
  c.la_estab,
  sp.provider_name,
  ga.type_of_establishment_name,
  ga.phase_of_education_name,

  SUM(CASE WHEN c.enrol_status IN ('C','F','O') AND c.nc_year_actual = 'R' THEN 1 ELSE 0 END) AS NCY_R,
  SUM(CASE WHEN c.enrol_status IN ('C','F','O') AND c.nc_year_actual = '1' THEN 1 ELSE 0 END) AS NCY_1,
  SUM(CASE WHEN c.enrol_status IN ('C','F','O') AND c.nc_year_actual = '2' THEN 1 ELSE 0 END) AS NCY_2,
  SUM(CASE WHEN c.enrol_status IN ('C','F','O') AND c.nc_year_actual = '3' THEN 1 ELSE 0 END) AS NCY_3,
  SUM(CASE WHEN c.enrol_status IN ('C','F','O') AND c.nc_year_actual = '4' THEN 1 ELSE 0 END) AS NCY_4,
  SUM(CASE WHEN c.enrol_status IN ('C','F','O') AND c.nc_year_actual = '5' THEN 1 ELSE 0 END) AS NCY_5,
  SUM(CASE WHEN c.enrol_status IN ('C','F','O') AND c.nc_year_actual = '6' THEN 1 ELSE 0 END) AS NCY_6,
  SUM(CASE WHEN c.enrol_status IN ('C','F','O') AND c.nc_year_actual = '7' THEN 1 ELSE 0 END) AS NCY_7,
  SUM(CASE WHEN c.enrol_status IN ('C','F','O') AND c.nc_year_actual = 'X' AND c.age_at_start_of_academic_year BETWEEN 5 AND 10 THEN 1 ELSE 0 END) AS NCY_X5to10

from {{ref('psg_scoped_providers_2425')}} sp
left join {{ref('stg_gias')}} ga on sp.urn = ga.urn
inner join {{ref('stg_census')}} c on ga.urn=c.urn

where c.academic_year = 202425 and c.census_date > DATE '2024-12-31' and c.census_date <= DATE '2025-01-31'

group by 
  c.academic_year,
  c.census_term,
  sp.urn,
  sp.ukprn,
  sp.la_number,
  sp.la_name,
  c.la_estab,
  sp.provider_name,
  ga.type_of_establishment_name,
  ga.phase_of_education_name

order by sp.urn