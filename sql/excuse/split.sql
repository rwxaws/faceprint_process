-- Split raw_duty into full day (≥7 hours) and half day (<7 hours)
INSERT INTO excuse_duty_full
SELECT * FROM raw_duty
WHERE num_hours >= 7;


INSERT INTO excuse_duty_half
SELECT * FROM raw_duty
WHERE num_hours < 7;


-- Split raw_rest into full day (has num_rest_days) and half day (has num_hours)
INSERT INTO excuse_rest_full
SELECT
    id,
    emp_voter_num,
    emp_name,
    num_rest_days,
    rest_start_date,
    rest_end_date,
    status
FROM raw_rest
WHERE num_rest_days IS NOT NULL;


INSERT INTO excuse_rest_half
SELECT
    id,
    emp_voter_num,
    emp_name,
    num_hours,
    start_hour,
    end_hour,
    date,
    status
FROM raw_rest
WHERE num_hours IS NOT NULL;
