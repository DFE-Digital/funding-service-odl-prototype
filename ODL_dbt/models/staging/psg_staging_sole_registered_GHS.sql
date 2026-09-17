WITH raw_csv AS (

    SELECT *
    FROM read_csv(
        'raw_data/ghs_approved_soleregbyage_all.csv',
        header = true,
        escape = '"',
        strict_mode = false,
        nullstr = 'null'
    )

) SELECT * FROM raw_csv