with raw_csv as(
    select * from 
    read_csv('raw_data/ukrlp.csv',
        header = true,
        escape = '"',
        strict_mode = false,
        all_varchar = true, -- read all values as varchar to avoid type conversion errors, convert later
        nullstr = 'null'    -- 'null' strings in csvs converted to SQL NULL values
    )
),
stg_ukrlp as (
    select
    --integers 
    try_cast(nullif(trim(UKPRN), '') as bigint) as ukprn,
    --dates
    strftime(try_strptime(nullif(trim(OPENDATE), ''), '%d/%m/%Y')::date, '%Y-%m-%d') as open_date,
    strftime(try_strptime(nullif(trim(CLOSEDATE), ''), '%d/%m/%Y')::date, '%Y-%m-%d') as close_date,
    --strings
    nullif(trim(Company_House_Number), '') as company_house_number,
    nullif(trim(LEGALNAME), '') as legal_name,
    nullif(trim("NAME"), '') as "name",
    nullif(trim(URN), '') as urn,
    nullif(trim(DataSourcePath), '') as data_source_path,
    nullif(trim(DataSourceID), '') as data_source_id,
    --boolean
    try_cast(nullif(trim(LIVE), '') as boolean) as live
    from raw_csv
)
select * from stg_ukrlp

