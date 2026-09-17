WITH GHS AS(
    SELECT
    '202526' as academic_year,
    'GHS - one census per academic year' as census_term,
    urn,
    ukprn,
    la_number,
    la_name,
    la_estab,
    provider_name,
    type_of_establishment_name,
    phase_of_education_name,
    0 as NCY_R,
    0 as NCY_1,
    0 as NCY_2,
    0 as NCY_3,
    0 as NCY_4,
    0 as NCY_5,
    0 as NCY_6,
    0 as NCY_7,
    0 as NCY_X5to10,
    Age5_Total,
    Age6_Total,
    Age7_Total,
    Age8_Total,
    Age9_Total,
    Age10_Total
    FROM{{ref('PSG_sole_and_dual_GHS_pupils_2526')}}
),
MAIN_REG AS(
    SELECT
    *,
    0 as Age5_Total,
    0 as Age6_Total,
    0 as Age7_Total,
    0 as Age8_Total,
    0 as Age9_Total,
    0 as Age10_Total
    FROM{{ref('PSG_sole_and_dual_main_registered_pupils_2526')}}
),
UNIONED AS(
    SELECT * FROM GHS
    UNION ALL
    SELECT * FROM MAIN_REG
    ORDER BY la_estab, ukprn
)
SELECT * FROM UNIONED