CREATE MASKING POLICY IF NOT EXISTS @schema.mp_last_name AS (
    masked_column string,
    first_name_column string
) RETURNS string ->
    CASE 
        WHEN masked_column IS NOT NULL THEN LEFT(first_name_column, 1)
        ELSE NULL
    END;