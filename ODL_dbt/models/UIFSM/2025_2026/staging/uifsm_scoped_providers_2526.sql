with raw_csv as (

    select * 
    from read_csv(
        'UIFSM/2025_2026/data/scoped_providers_uifsm_2526.csv',
        header = true,
        escape = '"',
        strict_mode = false,
        all_varchar = true, -- read all values as varchar to avoid type conversion errors, convert later
        nullstr = 'null'    -- 'null' strings in csvs converted to SQL NULL values
    )

),
stg_scoped_providers as (

    select
        --integers
        try_cast(nullif(trim("Provider.Ukprn"), '') as bigint) as ukprn,
        try_cast(nullif(trim("Provider.Urn"), '') as bigint) as urn,
        try_cast(nullif(trim("ProviderType.ProviderTypeCode"), '') as int) as provider_type_code,
        try_cast(nullif(trim("ProviderType.Store_ProviderTypeCode"), '') as int) as store_provider_type_code,
        try_cast(nullif(trim("ProviderSubType.ProviderSubtypeCode"), '') as int) as provider_subtype_code,
        try_cast(nullif(trim("ProviderSubType.Store_ProviderSubtypeCode"), '') as int) as store_provider_subtype_code,
        try_cast(nullif(trim("FurtherEducationType.Code"), '') as int) as further_education_type_code,
        try_cast(nullif(trim("Authority.Code"), '') as int) as la_number,
        try_cast(nullif(trim("ReasonEstablishmentOpened.Code"), '') as int) as reason_establishment_opened_code,
        try_cast(nullif(trim("PaymentOrganisation.Ukprn"), '') as bigint) as payment_organisation_ukprn,
        try_cast(nullif(trim("ReasonEstablishmentClosed.Code"), '') as int) as reason_establishment_closed_code,
        try_cast(nullif(trim("PaymentOrganisation.TrustCode"), '') as int) as payment_organisation_trust_code,
        try_cast(nullif(trim("PaymentOrganisation.Urn"), '') as bigint) as payment_organisation_urn,
        try_cast(nullif(trim("PaymentOrganisation.CompanyHouseNumber"), '') as bigint) as payment_organisation_company_house_number,
        
        try_cast(nullif(trim("ProviderStatus.Code"), '') as int) as provider_status_code,
        try_cast(nullif(trim("PhaseOfEducation.Code"), '') as int) as phase_of_education_code,
        try_cast(nullif(trim("Provider.StatutoryLowAge"), '') as int) as provider_statutory_low_age,
        try_cast(nullif(trim("Provider.StatutoryHighAge"), '') as int) as provider_statutory_high_age,
        try_cast(nullif(trim("Provider.EstablishmentNumber"), '') as bigint) as provider_establishment_number,
        try_cast(nullif(trim("Provider.DfeEstablishmentNumber"), '') as int) as provider_dfe_establishment_number,
        try_cast(nullif(trim("TrustStatus.Code"), '') as int) as trust_status_code,
        try_cast(nullif(trim("Provider.PreviousLaCode"), '') as int) as provider_previous_la_number,
        try_cast(nullif(trim("Provider.CensusWardCode"), '') as bigint) as provider_census_ward_code,
        
        --dates 
        try_cast(nullif(trim("Provider.DateOpened"), '') as date) as provider_date_opened,
        try_cast(nullif(trim("Provider.DateClosed"), '') as date) as provider_date_closed,

        --strings
        trim("PaymentOrganisation.GroupIdNumber") as payment_organisation_group_id_number,
        trim("Provider.WardCode") as provider_ward_code,
        trim("Provider.RscRegionCode") as provider_rsc_region_code,
        trim("Provider.GovernmentOfficeRegionCode") as provider_government_office_region_code,
        trim("Provider.DistrictCode") as provider_district_code,
        trim("Provider.MiddleSuperOutputAreaCode") as provider_middle_super_output_area_code,
        trim("Provider.LowerSuperOutputAreaCode") as provider_lower_super_output_area_code,
        trim("Provider.ParliamentaryConstituencyCode") as provider_parliamentary_constituency_code,
        trim("Provider.CountryCode") as provider_country_code,
        trim("Provider.OfficialSixthFormCode") as provider_official_sixth_form_code,
        trim("Provider.Name") as provider_name,
        trim("ProviderType.ProviderType") as provider_type,
        trim("ProviderType.Store_ProviderType") as store_provider_type,
        trim("ProviderSubType.ProviderSubtype") as provider_subtype,
        trim("ProviderSubType.Store_ProviderSubtype") as store_provider_subtype,
        trim("FurtherEducationType.FurtherEducationType") as further_education_type,
        trim("Authority.Authority") as la_name,
        trim("ReasonEstablishmentOpened.ReasonEstablishmentOpened") as reason_establishment_opened,
        trim("ReasonEstablishmentClosed.ReasonEstablishmentClosed") as reason_establishment_closed,
        trim("PaymentOrganisation.Name") as payment_organisation_name,
        trim("PaymentOrganisation.PaymentOrganisationType") as payment_organisation_type,
        trim("ProviderStatus.ProviderStatus") as provider_status,
        trim("PhaseOfEducation.PhaseOfEducation") as phase_of_education,
        trim("Provider.Postcode") as provider_postcode,
        trim("Provider.Town") as provider_town,
        trim("Provider.Street") as provider_street,
        trim("Provider.Locality") as provider_locality,
        trim("Provider.Address3") as provider_address3,
        trim("TrustStatus.TrustStatus") as trust_status,
        trim("Provider.PreviousLaName") as provider_previous_la_name,
        trim("Provider.PreviousEstablishmentNumber") as provider_previous_establishment_number,
        trim("Provider.RscRegionName") as provider_rsc_region_name,
        trim("Provider.GovernmentOfficeRegionName") as provider_government_office_region_name,
        trim("Provider.DistrictName") as provider_district_name,
        trim("Provider.WardName") as provider_ward_name,
        trim("Provider.CensusWardName") as provider_census_ward_name,
        trim("Provider.MiddleSuperOutputAreaName") as provider_middle_super_output_area_name,  
        trim("Provider.LowerSuperOutputAreaName") as provider_lower_super_output_area_name,
        trim("Provider.ParliamentaryConstituencyName") as provider_parliamentary_constituency_name,
        trim("Provider.CountryName") as provider_country_name,
        trim("Provider.OfficialSixthFormName") as provider_official_sixth_form_name,
        trim("Stream") as funding_stream,
        trim("Period") as scoping_period

    from raw_csv

)
select * from stg_scoped_providers