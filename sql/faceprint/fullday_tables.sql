CREATE OR REPLACE TABLE faceprint_duty_fullday AS
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
        dfd.id,
        dfd.num_hours,
        dfd.start_hour,
        dfd.end_hour,
        dfd.duty_date,
        dfd.status
    FROM
        faceprint AS fp
    INNER JOIN
        duty_fullday AS dfd
    ON
        fp.emp_voter_num = dfd.emp_voter_num;


CREATE OR REPLACE TABLE faceprint_restday AS
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
        rd.id,
        rd.num_rest_days,
        rd.rest_start_date,
        rd.rest_end_date,
        rd.status
    FROM
        faceprint AS fp
    INNER JOIN
        rest_day as rd
    ON
        fp.emp_voter_num = rd.emp_voter_num;


CREATE OR REPLACE TABLE faceprint_fullday AS
    SELECT * FROM faceprint_duty_fullday
    UNION ALL BY NAME
    SELECT * FROM faceprint_restday;


DELETE FROM
    faceprint
WHERE
    emp_voter_num IN (SELECT emp_voter_num FROM faceprint_fullday)
