CREATE OR REPLACE TABLE export_report_attendant AS
SELECT
    emp_voter_num,
    emp_name,
    date,
    unit,
    entry_time,
    leave_time,
    target_entry
FROM report_attendant;

CREATE OR REPLACE TABLE export_report_excused_full AS
SELECT
    emp_voter_num,
    emp_name,
    date,
    unit,
    is_absent,
    excuse,
    id,
    excuse_type,
    num_rest_days,
    rest_start_date,
    rest_end_date,
    duty_date,
    status
FROM report_excused_full;

CREATE OR REPLACE TABLE export_report_excused_half AS
SELECT
    emp_voter_num,
    emp_name,
    date,
    unit,
    entry_time,
    leave_time,
    target_entry,
    is_late,
    is_early,
    excuse,
    entry_excuse_id,
    entry_excuse_type,
    entry_num_hours,
    entry_start_hour,
    entry_end_hour,
    entry_status,
    leave_excuse_id,
    leave_excuse_type,
    leave_num_hours,
    leave_start_hour,
    leave_end_hour,
    leave_status
FROM report_excused_half;

-- no excuse or mismatched excuse
CREATE OR REPLACE TABLE export_report_unexcused AS
SELECT
    emp_voter_num,
    emp_name,
    date,
    unit,
    entry_time,
    leave_time,
    target_entry,
    is_late,
    is_early,
    is_absent,
    excuse,
    NULL AS mismatched_excuse_id,
    NULL AS mismatched_excuse_type,
    NULL AS mismatched_num_hours,
    NULL AS mismatched_start_hour,
    NULL AS mismatched_end_hour,
    NULL AS mismatched_status
FROM report
UNION ALL
SELECT
    emp_voter_num,
    emp_name,
    date,
    unit,
    entry_time,
    leave_time,
    target_entry,
    is_late,
    is_early,
    is_absent,
    excuse,
    mismatched_excuse_id,
    mismatched_excuse_type,
    mismatched_num_hours,
    mismatched_start_hour,
    mismatched_end_hour,
    mismatched_status
FROM report_excused_half_mismatched;
