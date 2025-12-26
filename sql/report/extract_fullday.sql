CREATE OR REPLACE TABLE report_excused_full AS
WITH
report_duty_full AS (
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
        df.id,
        'واجب يوم كامل' AS excuse_type,
        df.num_hours,
        df.start_hour,
        df.end_hour,
        df.duty_date,
        df.status
    FROM report AS rp
    INNER JOIN excuse_duty_full AS df ON rp.emp_voter_num = df.emp_voter_num
),

report_rest_full AS (
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
        'اجازة' AS excuse_type,
        rd.num_rest_days,
        rd.rest_start_date,
        rd.rest_end_date,
        rd.status
    FROM report AS rp
    INNER JOIN excuse_rest_full AS rd ON rp.emp_voter_num = rd.emp_voter_num
)

SELECT * FROM report_duty_full
UNION ALL BY NAME
SELECT * FROM report_rest_full;

DELETE FROM report
WHERE emp_voter_num IN (SELECT emp_voter_num FROM report_excused_full);
