CREATE OR REPLACE TABLE raw_duty (
    id VARCHAR,
    emp_voter_num VARCHAR,
    emp_name VARCHAR,
    num_hours INTEGER,
    start_hour TIME,
    end_hour VARCHAR,
    duty_date DATE,
    status VARCHAR
);

CREATE OR REPLACE TABLE raw_rest (
    id VARCHAR,
    emp_voter_num VARCHAR,
    emp_name VARCHAR,
    unit VARCHAR,
    rest_type VARCHAR,
    num_rest_days INTEGER,
    rest_start_date DATE,
    rest_end_date DATE,
    num_hours INTEGER,
    start_hour TIME,
    end_hour VARCHAR,
    date DATE,
    status VARCHAR
);

CREATE OR REPLACE TABLE excuse_duty_full (
    id VARCHAR,
    emp_voter_num VARCHAR,
    emp_name VARCHAR,
    num_hours INTEGER,
    start_hour TIME,
    end_hour TIME,
    duty_date DATE,
    status VARCHAR
);

CREATE OR REPLACE TABLE excuse_duty_half (
    id VARCHAR,
    emp_voter_num VARCHAR,
    emp_name VARCHAR,
    num_hours INTEGER,
    start_hour TIME,
    end_hour TIME,
    duty_date DATE,
    status VARCHAR
);

CREATE OR REPLACE TABLE excuse_rest_full (
    id VARCHAR,
    emp_voter_num VARCHAR,
    emp_name VARCHAR,
    num_rest_days INTEGER,
    rest_start_date DATE,
    rest_end_date DATE,
    status VARCHAR
);

CREATE OR REPLACE TABLE excuse_rest_half (
    id VARCHAR,
    emp_voter_num VARCHAR,
    emp_name VARCHAR,
    num_hours INTEGER,
    start_hour TIME,
    end_hour TIME,
    date DATE,
    status VARCHAR
);
