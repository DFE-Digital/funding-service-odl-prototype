 SELECT
    g.urn,
    g.ukprn,
    g.la_code as la_number,
    g.la_name,
    sr.laestab,
    g.establishment_name as provider_name,
    g.type_of_establishment_name,
    g.phase_of_education_name,
    COALESCE(sr.SRGirl5, 0)  + COALESCE(sr.SRBoy5, 0)  AS Age5_Total,
    COALESCE(sr.SRGirl6, 0)  + COALESCE(sr.SRBoy6, 0)  AS Age6_Total,
    COALESCE(sr.SRGirl7, 0)  + COALESCE(sr.SRBoy7, 0)  AS Age7_Total,
    COALESCE(sr.SRGirl8, 0)  + COALESCE(sr.SRBoy8, 0)  AS Age8_Total,
    COALESCE(sr.SRGirl9, 0)  + COALESCE(sr.SRBoy9, 0)  AS Age9_Total,
    COALESCE(sr.SRGirl10, 0) + COALESCE(sr.SRBoy10, 0) AS Age10_Total
    FROM {{ref('psg_staging_sole_registered_GHS')}} sr
    INNER JOIN {{ref('stg_gias')}} g ON  sr.la=g.la_code and sr.estab=g.establishment_number
    WHERE year = 2025 and la_number in (201,202,203)
ORDER BY sr.laestab
