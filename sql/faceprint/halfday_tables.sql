CREATE OR REPLACE TABLE faceprint_duty_halfday AS
    SELECT
        fp.emp_voter_num,
        fp.emp_name,
        fp.date,
        fp.emp_center_num,
        fp.entry_time,
        fp.leave_time,
        fp.target_entry,
        fp.is_late,
        fp.is_early,
        fp.is_absent,
        dhd.id,
        dhd.num_hours,
        dhd.start_hour,
        dhd.end_hour,
        dhd.duty_date,
        dhd.status
    FROM
        faceprint AS fp
    INNER JOIN
        duty_halfday AS dhd
    ON
        fp.emp_voter_num = dhd.emp_voter_num
    WHERE
        (
            fp.is_late IS NOT NULL AND
            fp.is_early IS NULL    AND
            fp.entry_time BETWEEN dhd.start_hour AND dhd.end_hour
        )
        OR
        (
            fp.is_early IS NOT NULL AND
            fp.is_late IS NULL      AND
            fp.leave_time BETWEEN dhd.start_hour AND dhd.end_hour
        )

CREATE OR REPLACE TABLE faceprint_resttime AS
    SELECT
        fp.emp_voter_num,
        fp.emp_name,
        fp.date,
        fp.emp_center_num,
        fp.entry_time,
        fp.leave_time,
        fp.target_entry,
        fp.is_late,
        fp.is_early,
        fp.is_absent,
        rt.id,
        rt.num_hours,
        rt.start_hour,
        rt.end_hour,
        rt.status
    FROM
        faceprint AS fp
    INNER JOIN
        rest_time AS rt
    ON
        fp.emp_voter_num = rt.emp_voter_num
    WHERE
        (
            fp.is_late  IS NOT NULL AND
            fp.is_early IS NULL     AND
            fp.entry_time BETWEEN rt.start_hour AND rt.end_hour
        )
        OR
        (
            fp.is_early IS NOT NULL AND
            fp.is_late  IS NULL     AND
            fp.leave_time BETWEEN rt.start_hour AND rt.end_hour
        );

CREATE OR REPLACE TABLE faceprint_halfday AS
    SELECT * FROM faceprint_duty_halfday
    UNION ALL BY NAME
    SELECT * FROM faceprint_resttime;

DELETE FROM
    faceprint
WHERE
    emp_voter_num IN (SELECT emp_voter_num from faceprint_halfday)
