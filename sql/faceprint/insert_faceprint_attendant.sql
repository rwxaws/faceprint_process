-- insert attendant
INSERT INTO
    faceprint_attendant
SELECT
    *
FROM
    faceprint
WHERE
    is_late IS NULL AND
    is_mid IS NULL AND
    is_early IS NULL AND
    is_absent IS NULL;

-- remove attendant from faceprint
DELETE FROM
    faceprint
WHERE
    is_late IS NULL AND
    is_mid IS NULL AND
    is_early IS NULL AND
    is_absent IS NULL;
