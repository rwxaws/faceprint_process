CREATE OR REPLACE TABLE faceprint (
    emp_voter_num   VARCHAR,
    emp_name        VARCHAR,
    date            DATE,
    emp_center_num  VARCHAR,
    entry_time      TIME,
    mid_time        TIME,
    leave_time      TIME,
    target_entry    TIME,
    target_mid      TIME,
    is_late         VARCHAR,
    is_mid          VARCHAR,
    is_early        VARCHAR,
    is_absent       VARCHAR
);

CREATE OR REPLACE TABLE faceprint_attendant (
    emp_voter_num   VARCHAR,
    emp_name        VARCHAR,
    date            DATE,
    emp_center_num  VARCHAR,
    entry_time      TIME,
    mid_time        TIME,
    leave_time      TIME,
    target_entry    TIME,
    target_mid      TIME,
    is_late         VARCHAR,
    is_mid          VARCHAR,
    is_early        VARCHAR,
    is_absent       VARCHAR
);
