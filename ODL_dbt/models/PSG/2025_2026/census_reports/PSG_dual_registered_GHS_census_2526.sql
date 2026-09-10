 SELECT

    g.urn,
    g.ukprn,
    g.la_code as la_number,
    g.la_name,
    cast(concat(cast(dr.la as string), cast(dr.estab as string)) as integer) as laestab,
    g.establishment_name as provider_name,
    g.type_of_establishment_name,
    g.phase_of_education_name,
    coalesce(dr.DRGirl5,0)+coalesce(dr.DRBoy5,0) as Age5_Total,
    coalesce(dr.DRGirl6,0)+coalesce(dr.DRBoy6,0) as Age6_Total,
    coalesce(dr.DRGirl7,0)+coalesce(dr.DRBoy7,0) as Age7_Total,
    coalesce(dr.DRGirl8,0)+coalesce(dr.DRBoy8,0) as Age8_Total,
    coalesce(dr.DRGirl9,0)+coalesce(dr.DRBoy9,0) as Age9_Total,
    coalesce(dr.DRGirl10,0)+coalesce(dr.DRBoy10,0) as Age10_Total
    FROM {{ref('psg_staging_dual_registered_GHS')}} dr 
    INNER JOIN {{ref('stg_gias')}} g ON  dr.la=g.la_code and dr.estab=g.establishment_number
    WHERE year = 2026 and la_number in (201,202,203)
ORDER BY laestab


