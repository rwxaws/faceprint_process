CREATE OR REPLACE TABLE faceprint_excused_full AS
WITH
faceprint_duty_full AS (
    SELECT
        fp.emp_voter_num,
        fp.emp_name,
        fp.date,
        fp.emp_center_num,
        fp.entry_time,
        fp.mid_time,
        fp.leave_time,
        fp.target_entry,
        fp.target_mid,
        fp.is_late,
        fp.is_mid,
        fp.is_early,
        fp.is_absent,
        df.id,
        'واجب يوم كامل' AS excuse_type,
        df.duty_date,
        df.status
    FROM faceprint AS fp
    INNER JOIN excuse_duty_full AS df ON fp.emp_voter_num = df.emp_voter_num
),

faceprint_rest_full AS (
    SELECT
        fp.emp_voter_num,
        fp.emp_name,
        fp.date,
        fp.emp_center_num,
        fp.entry_time,
        fp.mid_time,
        fp.leave_time,
        fp.target_entry,
        fp.target_mid,
        fp.is_late,
        fp.is_early,
        fp.is_absent,
        rd.id,
        'اجازة' AS excuse_type,
        rd.num_rest_days,
        rd.rest_start_date,
        rd.rest_end_date,
        rd.status
    FROM faceprint AS fp
    INNER JOIN excuse_rest_full AS rd ON fp.emp_voter_num = rd.emp_voter_num
)

SELECT * FROM faceprint_duty_full
UNION ALL BY NAME
SELECT * FROM faceprint_rest_full;

DELETE FROM faceprint
WHERE emp_voter_num IN (SELECT emp_voter_num FROM faceprint_excused_full);
