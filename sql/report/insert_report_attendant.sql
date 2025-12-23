-- insert attendants
INSERT INTO
    report_attendant
SELECT
    *
FROM
    report
WHERE
    is_late   IS NULL AND
    is_early  IS NULL AND
    is_absent IS NULL;

-- remove attendants from report
DELETE FROM
    report
WHERE
    is_late   IS NULL AND
    is_early  IS NULL AND
    is_absent IS NULL;
