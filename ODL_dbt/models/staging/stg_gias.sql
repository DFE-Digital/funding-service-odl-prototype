select *
from {{ source('gias', 'establishment_fields') }}