-- insert from dataframes
INSERT INTO raw_duty
SELECT *
FROM duty_df;

INSERT INTO raw_rest
SELECT *
FROM rest_df;
