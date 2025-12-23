-- report
INSERT INTO
    report
SELECT
    emp_voter_num,
    emp_name,
    strptime(date, '%Y-%d-%m %H:%M:%S')::DATE as date,
    unit,
    entry_time,
    leave_time,
    target_entry,
    NULL,
    NULL,
    NULL,
    excuse
FROM
    report_df;
