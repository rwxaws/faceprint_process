CREATE OR REPLACE TABLE report_duty_fullday AS
    SELECT
        rp.emp_voter_num,
        rp.emp_name,
        rp.date,
        rp.unit,
        rp.entry_time,
        rp.leave_time,
        rp.target_entry,
        rp.is_late,
        rp.is_early,
        rp.is_absent,
        rp.excuse,
        dfd.id,
        dfd.num_hours,
        dfd.start_hour,
        dfd.end_hour,
        dfd.duty_date,
        dfd.status
    FROM
        report AS rp
    INNER JOIN
        duty_fullday AS dfd
    ON
        rp.emp_voter_num = dfd.emp_voter_num;

CREATE OR REPLACE TABLE report_restday AS
    SELECT
        rp.emp_voter_num,
        rp.emp_name,
        rp.date,
        rp.unit,
        rp.entry_time,
        rp.leave_time,
        rp.target_entry,
        rp.is_late,
        rp.is_early,
        rp.is_absent,
        rp.excuse,
        rd.id,
        rd.num_rest_days,
        rd.rest_start_date,
        rd.rest_end_date,
        rd.status
    FROM
        report AS rp
    INNER JOIN
        rest_day AS rd
    ON
        rp.emp_voter_num = rd.emp_voter_num;


CREATE OR REPLACE TABLE report_fullday AS
    SELECT * FROM report_duty_fullday
    UNION ALL BY NAME
    SELECT * FROM report_restday;


DELETE FROM
    report
WHERE
    emp_voter_num IN (SELECT emp_voter_num FROM report_fullday)
