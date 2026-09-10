select 
academic_year,
census_term,
census_date,
cast(urn as integer) as urn,
cast(la_number as integer) as la_number,
cast(la_estab as integer) as la_estab,
enrol_status,
nc_year_actual,
age_at_start_of_academic_year,
cast(fsm_eligible as integer) as fsm_eligible,
school_lunch_taken
from {{ source('main', 'raw_census') }}