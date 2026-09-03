select 
sp.urn,
  c.la_estab,
  sp.ukprn,
  sp.la_number,
  sp.la_name, 
  sp.provider_name,
  ga.type_of_establishment_name,
  ga.phase_of_education_name,
SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = 'N1' THEN 1 ELSE 0 END) AS NCY_N1,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = 'N2' THEN 1 ELSE 0 END) AS NCY_N2,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = 'R' THEN 1 ELSE 0 END) AS NCY_R,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = '1' THEN 1 ELSE 0 END) AS NCY_1,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = '2' THEN 1 ELSE 0 END) AS NCY_2,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = 'X' AND c.age_at_start_of_academic_year =4 THEN 1 ELSE 0 END) AS NCY_X4,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = 'X' AND c.age_at_start_of_academic_year =5 THEN 1 ELSE 0 END) AS NCY_X5,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = 'X' AND c.age_at_start_of_academic_year =6 THEN 1 ELSE 0 END) AS NCY_X6,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = 'N1'AND c.fsm_eligible ='1' THEN 1 ELSE 0 END) AS FSM_NCY_N1,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = 'N2'AND c.fsm_eligible ='1' THEN 1 ELSE 0 END) AS FSM_NCY_N2,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = 'R'AND c.fsm_eligible ='1' THEN 1 ELSE 0 END) AS FSM_NCY_R,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = '1'AND c.fsm_eligible ='1' THEN 1 ELSE 0 END) AS FSM_NCY_1,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = '2'AND c.fsm_eligible ='1' THEN 1 ELSE 0 END) AS FSM_NCY_2,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = 'X' AND c.age_at_start_of_academic_year =4 AND c.fsm_eligible='1' THEN 1 ELSE 0 END) AS FSM_NCY_X4,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = 'X' AND c.age_at_start_of_academic_year =5 AND c.fsm_eligible='1' THEN 1 ELSE 0 END) AS FSM_NCY_X5,
  SUM(CASE WHEN c.enrol_status IN ('C','M') AND c.nc_year_actual = 'X' AND c.age_at_start_of_academic_year =6 AND c.fsm_eligible='1' THEN 1 ELSE 0 END) AS FSM_NCY_X6

from {{ref('uifsm_scoped_providers_2526')}} sp
left join {{ref('stg_gias')}} ga on sp.urn = ga.urn
inner join {{ref('stg_census')}} c on ga.urn=c.urn

where c.academic_year = 202526 and c.census_date > DATE '2025-09-30' and c.census_date <= DATE '2025-10-31'
and ga.la_code !=207

group by
sp.urn,
  c.la_estab,
  sp.ukprn,
  sp.la_number,
  sp.la_name, 
  sp.provider_name,
  ga.type_of_establishment_name,
  ga.phase_of_education_name

HAVING NOT (
       NCY_N1 = 0
   AND NCY_N2 = 0
   AND NCY_R  = 0
   AND NCY_1  = 0
   AND NCY_2  = 0
   AND NCY_X4 = 0
   AND NCY_X5 = 0
   AND NCY_X6 = 0
   AND FSM_NCY_N1 = 0
   AND FSM_NCY_N2 = 0
   AND FSM_NCY_R  = 0
   AND FSM_NCY_1  = 0
   AND FSM_NCY_2  = 0
   AND FSM_NCY_X4 = 0
   AND FSM_NCY_X5 = 0
   AND FSM_NCY_X6 = 0
)

order by c.la_estab
