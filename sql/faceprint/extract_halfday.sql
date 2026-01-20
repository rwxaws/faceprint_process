-- combine rest and duty excuses
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
CREATE TABLE tmp_entry_match AS
SELECT
    fp.emp_voter_num,
    e.id AS entry_excuse_id,
    e.excuse_type AS entry_excuse_type,
    e.num_hours AS entry_num_hours,
    e.start_hour AS entry_start_hour,
    e.end_hour AS entry_end_hour,
    e.status AS entry_status
FROM faceprint AS fp
INNER JOIN tmp_excuses AS e
    ON
        fp.emp_voter_num = e.emp_voter_num
        AND fp.entry_time BETWEEN e.start_hour AND e.end_hour
        AND e.start_hour = fp.target_entry
WHERE fp.is_late IS NOT NULL;

-- mid excuse
CREATE TABLE tmp_mid_match AS
SELECT
    fp.emp_voter_num,
    e.id AS mid_excuse_id,
    e.excuse_type AS mid_excuse_type,
    e.num_hours AS mid_num_hours,
    e.start_hour AS mid_start_hour,
    e.end_hour AS mid_end_hour,
    e.status AS mid_status
FROM faceprint AS fp
INNER JOIN tmp_excuses AS e
    ON
        fp.emp_voter_num = e.emp_voter_num
        AND (
            (fp.mid_time IS NULL AND fp.target_mid BETWEEN e.start_hour AND e.end_hour)
            OR
            (fp.mid_time IS NOT NULL AND fp.mid_time BETWEEN e.start_hour AND e.end_hour)
        )
WHERE fp.is_mid IS NOT NULL;

-- leave excuse for early employees
CREATE OR REPLACE TABLE tmp_leave_match AS
SELECT
    fp.emp_voter_num,
    e.id AS leave_excuse_id,
    e.excuse_type AS leave_excuse_type,
    e.num_hours AS leave_num_hours,
    e.start_hour AS leave_start_hour,
    e.end_hour AS leave_end_hour,
    e.status AS leave_status
FROM faceprint AS fp
INNER JOIN tmp_excuses AS e
    ON
        fp.emp_voter_num = e.emp_voter_num
        AND fp.leave_time BETWEEN e.start_hour AND e.end_hour
        AND e.end_hour >= fp.target_entry + 7 * INTERVAL 1 HOUR
WHERE fp.is_early IS NOT NULL;

-- create employees that are excused for all three (entry,mid,leave)
CREATE OR REPLACE TABLE faceprint_excused_half AS
SELECT
    fp.*,
    em.entry_excuse_id,
    em.entry_excuse_type,
    em.entry_num_hours,
    em.entry_start_hour,
    em.entry_end_hour,
    em.entry_status,
    mm.mid_excuse_id,
    mm.mid_excuse_type,
    mm.mid_num_hours,
    mm.mid_start_hour,
    mm.mid_end_hour,
    mm.mid_status,
    lm.leave_excuse_id,
    lm.leave_excuse_type,
    lm.leave_num_hours,
    lm.leave_start_hour,
    lm.leave_end_hour,
    lm.leave_status
FROM faceprint AS fp
LEFT JOIN tmp_entry_match AS em ON fp.emp_voter_num = em.emp_voter_num
LEFT JOIN tmp_mid_match AS mm ON fp.emp_voter_num = mm.emp_voter_num
LEFT JOIN tmp_leave_match AS lm ON fp.emp_voter_num = lm.emp_voter_num
WHERE
    (fp.is_absent IS NULL)
    AND
    (fp.is_late IS NULL OR em.entry_excuse_id IS NOT NULL)
    AND
    (fp.is_mid IS NULL OR mm.mid_excuse_id IS NOT NULL)
    AND
    (fp.is_early IS NULL OR lm.leave_excuse_id IS NOT NULL);

-- Mismatched: employees with violations who have excuses but those excuses don't cover their violations
CREATE OR REPLACE TABLE faceprint_excused_half_mismatched AS
SELECT
    fp.*,
    e.id AS mismatched_excuse_id,
    e.excuse_type AS mismatched_excuse_type,
    e.num_hours AS mismatched_num_hours,
    e.start_hour AS mismatched_start_hour,
    e.end_hour AS mismatched_end_hour,
    e.status AS mismatched_status
FROM faceprint AS fp
INNER JOIN tmp_excuses AS e ON fp.emp_voter_num = e.emp_voter_num
WHERE
    fp.is_absent IS NULL
    AND fp.emp_voter_num NOT IN (SELECT emp_voter_num FROM faceprint_excused_half);

-- remove excused employees from faceprint
DELETE FROM faceprint
WHERE emp_voter_num IN (SELECT emp_voter_num FROM faceprint_excused_half);

-- remove mismatched employees from faceprint (they'll be in their own export table)
DELETE FROM faceprint
WHERE emp_voter_num IN (SELECT emp_voter_num FROM faceprint_excused_half_mismatched);
