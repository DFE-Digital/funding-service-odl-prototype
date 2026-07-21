select *
from {{ source('main', 'raw_census') }}