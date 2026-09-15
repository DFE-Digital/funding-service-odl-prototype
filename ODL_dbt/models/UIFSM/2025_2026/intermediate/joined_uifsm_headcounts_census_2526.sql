with joined as (

    select
        -- using coalesce to be extra sure we have all providers included across both census periods, even if they are only present in one of the two datasets
        coalesce(oct.academic_year, jan.academic_year) as academic_year,
        --don't need census term as we are just looking for the max value across the two census periods
        coalesce(oct.urn, jan.urn) as urn,
        coalesce(oct.la_estab, jan.la_estab) as la_estab,
        coalesce(oct.ukprn, jan.ukprn) as ukprn,
        coalesce(oct.la_number, jan.la_number) as la_number,
        coalesce(oct.la_name, jan.la_name) as la_name,
        coalesce(oct.provider_name, jan.provider_name) as provider_name,
        coalesce(oct.type_of_establishment_name, jan.type_of_establishment_name) as type_of_establishment_name,
        coalesce(oct.phase_of_education_name, jan.phase_of_education_name) as phase_of_education_name,
        --rest of columns from oct census as is, then rest of columns from jan census with jan suffix
        oct.*,
        jan.NCY_N1 as NCY_N1_jan,
        jan.NCY_N2 as NCY_N2_jan,
        jan.NCY_R as NCY_R_jan,
        jan.NCY_1 as NCY_1_jan,
        jan.NCY_2 as NCY_2_jan,
        jan.NCY_X4 as NCY_X4_jan,
        jan.NCY_X5 as NCY_X5_jan,
        jan.NCY_X6 as NCY_X6_jan,
        jan.FSM_NCY_N1 as FSM_NCY_N1_jan,
        jan.FSM_NCY_N2 as FSM_NCY_N2_jan,
        jan.FSM_NCY_R as FSM_NCY_R_jan, 
        jan.FSM_NCY_1 as FSM_NCY_1_jan,
        jan.FSM_NCY_2 as FSM_NCY_2_jan,
        jan.FSM_NCY_X4 as FSM_NCY_X4_jan,
        jan.FSM_NCY_X5 as FSM_NCY_X5_jan,
        jan.FSM_NCY_X6 as FSM_NCY_X6_jan

    from {{ ref('UIFSM_headcounts_oct_2025_census') }} oct
    full outer join {{ ref('UIFSM_headcounts_jan_2026_census') }} jan
        on oct.urn = jan.urn

)

select
    academic_year,
    urn,
    la_estab,
    ukprn,
    la_number,
    la_name,
    provider_name,
    type_of_establishment_name,
    phase_of_education_name,

    NCY_N1,
    FSM_NCY_N1,
    NCY_N1 - FSM_NCY_N1 as total_uifsm_meals_N1,
    NCY_N2,
    FSM_NCY_N2,
    NCY_N2 - FSM_NCY_N2 as total_uifsm_meals_N2,
    NCY_R,
    FSM_NCY_R,
    NCY_R - FSM_NCY_R as total_uifsm_meals_R,
    NCY_1,
    FSM_NCY_1,
    NCY_1 - FSM_NCY_1 as total_uifsm_meals_1,
    NCY_2,
    FSM_NCY_2,  
    NCY_2 - FSM_NCY_2 as total_uifsm_meals_2,
    NCY_X4,
    FSM_NCY_X4,
    NCY_X4 - FSM_NCY_X4 as total_uifsm_meals_X4,
    NCY_X5,     
    FSM_NCY_X5,
    NCY_X5 - FSM_NCY_X5 as total_uifsm_meals_X5,
    NCY_X6,
    FSM_NCY_X6,
    NCY_X6 - FSM_NCY_X6 as total_uifsm_meals_X6,

    NCY_N1_jan,
    FSM_NCY_N1_jan,
    NCY_N1_jan - FSM_NCY_N1_jan as total_uifsm_meals_N1_jan,
    NCY_N2_jan,
    FSM_NCY_N2_jan,
    NCY_N2_jan - FSM_NCY_N2_jan as total_uifsm_meals_N2_jan,
    NCY_R_jan,
    FSM_NCY_R_jan,
    NCY_R_jan - FSM_NCY_R_jan as total_uifsm_meals_R_jan,
    NCY_1_jan,
    FSM_NCY_1_jan,
    NCY_1_jan - FSM_NCY_1_jan as total_uifsm_meals_1_jan,
    NCY_2_jan,
    FSM_NCY_2_jan,
    NCY_2_jan - FSM_NCY_2_jan as total_uifsm_meals_2_jan,
    NCY_X4_jan,
    FSM_NCY_X4_jan,
    NCY_X4_jan - FSM_NCY_X4_jan as total_uifsm_meals_X4_jan,
    NCY_X5_jan,     
    FSM_NCY_X5_jan,
    NCY_X5_jan - FSM_NCY_X5_jan as total_uifsm_meals_X5_jan,
    NCY_X6_jan,
    FSM_NCY_X6_jan,
    NCY_X6_jan - FSM_NCY_X6_jan as total_uifsm_meals_X6_jan
from joined

