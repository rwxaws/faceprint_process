CREATE OR REPLACE TABLE duty_staging (
    id            VARCHAR,
    emp_voter_num VARCHAR,
    emp_name      VARCHAR,
    num_hours     INTEGER,
    start_hour    TIME,
    end_hour      VARCHAR,
    duty_date     DATE,
    status        VARCHAR
);

CREATE OR REPLACE TABLE rest_staging (
    id              VARCHAR,
    emp_voter_num   VARCHAR,
    emp_name        VARCHAR,
    unit            VARCHAR,
    rest_type       VARCHAR,
    num_rest_days   INTEGER,
    rest_start_date DATE,
    rest_end_date   DATE,
    num_hours       INTEGER,
    start_hour      TIME,
    end_hour        VARCHAR,
    date            DATE,
    status          VARCHAR
);

CREATE OR REPLACE TABLE duty_fullday (
    id            VARCHAR,
    emp_voter_num VARCHAR,
    emp_name      VARCHAR,
    num_hours     INTEGER,
    start_hour    TIME,
    end_hour      TIME,
    duty_date     DATE,
    status        VARCHAR
);

CREATE OR REPLACE TABLE duty_halfday (
    id            VARCHAR,
    emp_voter_num VARCHAR,
    emp_name      VARCHAR,
    num_hours     INTEGER,
    start_hour    TIME,
    end_hour      TIME,
    duty_date     DATE,
    status        VARCHAR
);

CREATE OR REPLACE TABLE rest_day (
   id              VARCHAR,
   emp_voter_num   VARCHAR,
   emp_name        VARCHAR,
   num_rest_days   INTEGER,
   rest_start_date DATE,
   rest_end_date   DATE,
   status          VARCHAR
);

CREATE OR REPLACE TABLE rest_time (
    id              VARCHAR,
    emp_voter_num   VARCHAR,
    emp_name        VARCHAR,
    num_hours       INTEGER,
    start_hour      TIME,
    end_hour        TIME,
    date            DATE,
    status          VARCHAR
);
