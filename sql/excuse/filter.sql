DELETE FROM excuse_duty_full
WHERE duty_date != getvariable('target_date')::DATE;

DELETE FROM excuse_duty_half
WHERE duty_date != getvariable('target_date')::DATE;

DELETE FROM excuse_rest_full
WHERE
    getvariable('target_date')::DATE < rest_start_date::DATE
    OR getvariable('target_date')::DATE > rest_end_date::DATE;

DELETE FROM excuse_rest_half
WHERE date != getvariable('target_date')::DATE;
