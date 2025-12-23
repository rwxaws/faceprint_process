DELETE FROM report
USING (
    SELECT emp_voter_num FROM report_duty_fullday
    UNION ALL
    SELECT emp_voter_num FROM report_duty_halfday
    UNION ALL
    SELECT emp_voter_num FROM report_restday
    UNION ALL
    SELECT emp_voter_num FROM report_resttime
    UNION ALL
    SELECT emp_voter_num FROM report_duty_halfday_missing
    UNION ALL
    SELECT emp_voter_num FROM report_resttime_missing
) x
WHERE
    report.emp_voter_num = x.emp_voter_num
