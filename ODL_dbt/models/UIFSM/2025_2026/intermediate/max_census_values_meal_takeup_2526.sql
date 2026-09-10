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
        jan.NCY_R as NCY_R_jan,
        jan.NCY_1 as NCY_1_jan,
        jan.NCY_2 as NCY_2_jan,
        jan.NCY_X4 as NCY_X4_jan,
        jan.NCY_X5 as NCY_X5_jan,
        jan.NCY_X6 as NCY_X6_jan,
        jan.FSM_NCY_R as FSM_NCY_R_jan, 
        jan.FSM_NCY_1 as FSM_NCY_1_jan,
        jan.FSM_NCY_2 as FSM_NCY_2_jan,
        jan.FSM_NCY_X4 as FSM_NCY_X4_jan,
        jan.FSM_NCY_X5 as FSM_NCY_X5_jan,
        jan.FSM_NCY_X6 as FSM_NCY_X6_jan

    from {{ ref('UIFSM_meal_takeup_oct_2025_census') }} oct
    full outer join {{ ref('UIFSM_meal_takeup_jan_2026_census') }} jan
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
    -- max values of the 2 censuses - ensures providers have enough funding
    greatest(coalesce(NCY_R, 0), coalesce(NCY_R_jan, 0)) as NCY_R,
    greatest(coalesce(NCY_1, 0), coalesce(NCY_1_jan, 0)) as NCY_1,
    greatest(coalesce(NCY_2, 0), coalesce(NCY_2_jan, 0)) as NCY_2,
    greatest(coalesce(NCY_X4, 0), coalesce(NCY_X4_jan, 0)) as NCY_X4,
    greatest(coalesce(NCY_X5, 0), coalesce(NCY_X5_jan, 0)) as NCY_X5,
    greatest(coalesce(NCY_X6, 0), coalesce(NCY_X6_jan, 0)) as NCY_X6,
    greatest(coalesce(FSM_NCY_R, 0), coalesce(FSM_NCY_R_jan, 0)) as FSM_NCY_R,
    greatest(coalesce(FSM_NCY_1, 0), coalesce(FSM_NCY_1_jan, 0)) as FSM_NCY_1,
    greatest(coalesce(FSM_NCY_2, 0), coalesce(FSM_NCY_2_jan, 0)) as FSM_NCY_2,
    greatest(coalesce(FSM_NCY_X4, 0), coalesce(FSM_NCY_X4_jan, 0)) as FSM_NCY_X4,
    greatest(coalesce(FSM_NCY_X5, 0), coalesce(FSM_NCY_X5_jan, 0)) as FSM_NCY_X5,
    greatest(coalesce(FSM_NCY_X6, 0), coalesce(FSM_NCY_X6_jan, 0)) as FSM_NCY_X6

from joined