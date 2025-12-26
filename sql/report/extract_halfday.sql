-- Combine duty_halfday and rest_time into unified excuse table
CREATE OR REPLACE TABLE tmp_excuses AS
SELECT
    emp_voter_num,
    id,
    'واجب' AS excuse_type,
    num_hours,
    start_hour,
    end_hour,
    status
FROM excuse_duty_half
UNION ALL
SELECT
    emp_voter_num,
    id,
    'زمنية' AS excuse_type,
    num_hours,
    start_hour,
    end_hour,
    status
FROM excuse_rest_half;

-- entry excuse for late employees
CREATE OR REPLACE TABLE tmp_entry_match AS
SELECT
    r.emp_voter_num,
    e.id AS entry_excuse_id,
    e.excuse_type AS entry_excuse_type,
    e.num_hours AS entry_num_hours,
    e.start_hour AS entry_start_hour,
    e.end_hour AS entry_end_hour,
    e.status AS entry_status
FROM report AS r
INNER JOIN tmp_excuses AS e
    ON
        r.emp_voter_num = e.emp_voter_num
        AND r.entry_time BETWEEN e.start_hour AND e.end_hour
        AND e.start_hour BETWEEN r.target_entry AND r.target_entry
        + 30 * INTERVAL 1 MINUTE
WHERE r.is_late IS NOT NULL;

-- leave excuse for early employees
CREATE OR REPLACE TABLE tmp_leave_match AS
SELECT
    r.emp_voter_num,
    e.id AS leave_excuse_id,
    e.excuse_type AS leave_excuse_type,
    e.num_hours AS leave_num_hours,
    e.start_hour AS leave_start_hour,
    e.end_hour AS leave_end_hour,
    e.status AS leave_status
FROM report AS r
INNER JOIN tmp_excuses AS e
    ON
        r.emp_voter_num = e.emp_voter_num
        AND r.leave_time BETWEEN e.start_hour AND e.end_hour
        AND e.end_hour >= r.target_entry + 7 * INTERVAL 1 HOUR
WHERE r.is_early IS NOT NULL;

-- Final: one row per employee, only if ALL violations are excused
CREATE OR REPLACE TABLE report_excused_half AS
SELECT
    r.*,
    em.entry_excuse_id,
    em.entry_excuse_type,
    em.entry_num_hours,
    em.entry_start_hour,
    em.entry_end_hour,
    em.entry_status,
    lm.leave_excuse_id,
    lm.leave_excuse_type,
    lm.leave_num_hours,
    lm.leave_start_hour,
    lm.leave_end_hour,
    lm.leave_status
FROM report AS r
LEFT JOIN tmp_entry_match AS em ON r.emp_voter_num = em.emp_voter_num
LEFT JOIN tmp_leave_match AS lm ON r.emp_voter_num = lm.emp_voter_num
WHERE
    (r.is_absent IS NULL)
    AND
    (r.is_late IS NULL OR em.entry_excuse_id IS NOT NULL)
    AND
    (r.is_early IS NULL OR lm.leave_excuse_id IS NOT NULL);

-- Remove excused employees from report
DELETE FROM report
WHERE emp_voter_num IN (SELECT emp_voter_num FROM report_excused_half);
