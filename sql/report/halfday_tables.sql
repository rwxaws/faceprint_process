-- only contains employees that are either late arriving or late leaving but not both

CREATE OR REPLACE TABLE report_duty_halfday AS
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
        dhd.id,
        dhd.num_hours,
        dhd.start_hour,
        dhd.end_hour,
        dhd.duty_date,
        dhd.status
    FROM
        report AS rp
    INNER JOIN
        duty_halfday AS dhd
    ON
        rp.emp_voter_num = dhd.emp_voter_num
    WHERE
        (
            rp.is_late IS NOT NULL    AND
            rp.is_early IS NULL       AND
            rp.entry_time BETWEEN dhd.start_hour AND dhd.end_hour
        )
        OR
        (
            rp.is_early IS NOT NULL   AND
            rp.is_late IS NULL        AND
            rp.leave_time BETWEEN dhd.start_hour AND dhd.end_hour
        );


CREATE OR REPLACE TABLE report_resttime AS
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
        rt.id,
        rt.num_hours,
        rt.start_hour,
        rt.end_hour,
        rt.status
    FROM
        report AS rp
    INNER JOIN
        rest_time AS rt
    ON
        rp.emp_voter_num = rt.emp_voter_num
    WHERE
        (
            rp.is_late  IS NOT NULL AND
            rp.is_early IS NULL     AND
            rp.entry_time BETWEEN rt.start_hour AND rt.end_hour
        )
        OR
        (
            rp.is_early IS NOT NULL AND
            rp.is_late  IS NULL     AND
            rp.leave_time BETWEEN rt.start_hour AND rt.end_hour
        );


CREATE OR REPLACE TABLE report_halfday AS
    SELECT * FROM report_duty_halfday
    UNION ALL BY NAME
    SELECT * FROM report_resttime;


DELETE FROM
    report
WHERE
    emp_voter_num IN (SELECT emp_voter_num FROM report_halfday);

