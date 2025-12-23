INSERT INTO
    duty_fullday
SELECT
    *
FROM
    duty_staging
WHERE
    num_hours >= 7;

INSERT INTO
    duty_halfday
SELECT
    *
FROM
    duty_staging
WHERE
    num_hours < 7;

INSERT INTO
    rest_day
SELECT
    id,
    emp_voter_num,
    emp_name,
    num_rest_days,
    rest_start_date,
    rest_end_date,
    status
FROM
    rest_staging
WHERE
    num_rest_days IS NOT NULL;

INSERT INTO
    rest_time
SELECT
    id,
    emp_voter_num,
    emp_name,
    num_hours,
    start_hour,
    end_hour,
    date,
    status
FROM
    rest_staging
WHERE
    num_hours IS NOT NULL;
