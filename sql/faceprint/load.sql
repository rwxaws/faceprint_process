INSERT INTO faceprint
SELECT
    emp_voter_num,
    emp_name,
    date,
    emp_center_num,
    entry_time,
    mid_time,
    leave_time,
    target_entry,
    target_mid,
    is_late,
    is_mid,
    is_early,
    is_absent
FROM faceprint_df;
