CREATE MASKING POLICY IF NOT EXISTS @schema.mp_first_name AS (
    masked_column string
) RETURNS string ->
    LEFT(CASE 
        WHEN masked_column IS NOT NULL THEN LEFT(masked_column, 3)
        ELSE NULL
    END || '**********', 10);