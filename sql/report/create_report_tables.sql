CREATE OR REPLACE TABLE report (
    emp_voter_num VARCHAR,
    emp_name      VARCHAR,
    date          DATE,
    unit          VARCHAR,
    entry_time    TIME,
    leave_time    TIME,
    target_entry  TIME,
    is_late       VARCHAR,
    is_early      VARCHAR,
    is_absent     VARCHAR,
    excuse        VARCHAR
);

CREATE OR REPLACE TABLE report_attendant (
    emp_voter_num VARCHAR,
    emp_name      VARCHAR,
    date          DATE,
    unit          VARCHAR,
    entry_time    TIME,
    leave_time    TIME,
    target_entry  TIME,
    is_late       VARCHAR,
    is_early      VARCHAR,
    is_absent     VARCHAR,
    excuse        VARCHAR
);
