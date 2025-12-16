import pandas as pd


def get_date(con, table_name):
    return str(con.sql(f"SELECT date FROM {table_name}").fetchone()[0])


def normalize_time(con, table_name, column_name):
    # converts written time into real time
    # 10AM  -> 10:00
    # 10:30 -> 10:30
    con.sql(f"""
        UPDATE {table_name}
        SET {column_name} = CASE
            WHEN LENGTH(SPLIT_PART({column_name}, ' ', 1)) <= 2
            THEN SPLIT_PART({column_name}, ' ', 1) || ':00' || ':00'
            ELSE SPLIT_PART({column_name}, ' ', 1) || ':00'
        END;
    """)


def military_time(con, table_name, column_name):
    # converts time into military time
    # 02:00:00 -> 14:00:00

    col_type = con.sql(f"""
        SELECT data_type
        FROM information_schema.columns
        WHERE
            table_name  = '{table_name}' AND
            column_name = '{column_name}'
    """).fetchone()[0]

    if (col_type == "VARCHAR"):
        con.sql(f"""
            UPDATE {table_name}
            SET {column_name} =
            CASE
                WHEN SPLIT_PART({column_name}, ':', 1)::INTEGER BETWEEN 1 AND 7
                THEN SPLIT_PART({column_name}, ':', 1)::INTEGER + 12 || ':' || SPLIT_PART({column_name}, ':', 2)
                ELSE {column_name}
            END
        """)

    if (col_type == "TIME"):
        con.sql(f"""
            UPDATE {table_name}
            SET {column_name} =
            CASE
                WHEN SPLIT_PART({column_name}::VARCHAR, ':', 1)::INTEGER BETWEEN 1 AND 7
                THEN (SPLIT_PART({column_name}::VARCHAR, ':', 1)::INTEGER + 12 || ':' || SPLIT_PART({column_name}::VARCHAR, ':', 2) || ':00')::TIME
                ELSE {column_name}
            END
        """)


def clean_duty(con, duty_file):
    con.sql("""
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
    """)

    duty_df = pd.read_excel(
        duty_file,
        skiprows=1,
        usecols="A:C,J:L,N:O",
        header=None,
        dtype=str
    )

    con.sql("""
        INSERT INTO duty_staging
        SELECT * FROM duty_df;
    """)

    # fix start & end_hour
    normalize_time(con, "duty_staging", "end_hour")

    # military_time(con, "duty_staging", "start_hour")
    military_time(con, "duty_staging", "end_hour")

    con.sql("""
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
    """)

    con.sql("""
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
    """)

    con.sql("""
        INSERT INTO duty_fullday
            SELECT * FROM duty_staging
            WHERE num_hours >= 7
    """)

    con.sql("""
        INSERT INTO duty_halfday
            SELECT * FROM duty_staging
            WHERE num_hours < 7
    """)

    con.sql("DROP TABLE duty_staging")


def clean_rest(con, rest_files):
    con.sql("""
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
    """)

    for file in rest_files:
        rest_df = pd.read_excel(
            file,
            skiprows=1,
            usecols="A:C,G,I:O,Q:R",
            header=None,
            dtype=str
        )
        con.sql("INSERT INTO rest_staging SELECT * FROM rest_df")

    # fix start_hour & end_hour
    normalize_time(con, "rest_staging", "end_hour")
    military_time(con, "rest_staging", "start_hour")
    military_time(con, "rest_staging", "end_hour")

    con.sql("""
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
    """)

    con.sql("""
        INSERT INTO rest_time
        SELECT
            id,
            emp_voter_num,
            emp_name,
            num_hours,
            start_hour,
            end_hour,
            date,
            status
        FROM rest_staging
        WHERE num_hours IS NOT NULL;
    """)

    con.sql("""
       CREATE OR REPLACE TABLE rest_day (
           id              VARCHAR,
           emp_voter_num   VARCHAR,
           emp_name        VARCHAR,
           num_rest_days   INTEGER,
           rest_start_date DATE,
           rest_end_date   DATE,
           status          VARCHAR
       );
    """)

    con.sql("""
        INSERT INTO rest_day
        SELECT
            id,
            emp_voter_num,
            emp_name,
            num_rest_days,
            rest_start_date,
            rest_end_date,
            status
        FROM rest_staging
        WHERE num_rest_days IS NOT NULL;
    """)


def clean_faceprint(con, faceprint_file):
    faceprint_df = pd.read_csv(
        faceprint_file,
        header=0,
        dtype=str
    )

    con.sql("""
        CREATE OR REPLACE TABLE faceprint
        (
            emp_voter_num   VARCHAR,
            emp_name        VARCHAR,
            date            DATE,
            emp_center_num  VARCHAR,
            entry_time      TIME,
            leave_time      TIME,
            target_entry    TIME,
            is_late         VARCHAR,
            is_early        VARCHAR,
            is_absent       VARCHAR
        );
    """)

    con.sql("INSERT INTO faceprint SELECT * FROM faceprint_df")


def clean_report(con, report_file, emp_file):
    report_df = pd.read_excel(
        report_file,
        header=None,
        skiprows=1,
        usecols="B:E,I:J",
        dtype=str
    )

    target_entry = pd.read_excel(
        report_file,
        header=None,
        usecols="M",
        dtype=str
    )[12][0]

    emp_df = pd.read_excel(
        emp_file,
        header=None,
        skiprows=1,
        usecols="A",
        dtype=str
    )

    report_df["target_entry"] = target_entry
    report_df["emp_voter_num"] = emp_df[0]

    report_columns = [
        "emp_name",
        "date",
        "entry_time",
        "leave_time",
        "excuse",
        "unit",
        "target_entry",
        "emp_voter_num"
    ]

    report_df.columns = report_columns

    if len(report_df) != len(emp_df):
        return False

    con.sql("""
        CREATE OR REPLACE TABLE report(
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
    """)

    con.sql("""
        CREATE OR REPLACE TABLE report_present(
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
    """)

    con.sql("""
        INSERT INTO report
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
        FROM report_df;
    """)

    # set absent
    con.sql("""
        UPDATE report
        SET is_absent = 'غائب'
        WHERE entry_time IS NULL AND leave_time IS NULL;
    """)

    # set without entry
    con.sql("""
        UPDATE report
        SET is_late = 'بدون بصمة دخول'
        WHERE entry_time IS NULL AND is_absent IS NULL;
    """)

    # set without leave
    con.sql("""
        UPDATE report
        SET is_early = 'بدون بصمة خروج'
        WHERE leave_time IS NULL AND is_absent IS NULL;
    """)

    # set late entry
    con.sql("""
        UPDATE report
        SET is_late = 'متأخر'
        WHERE
            entry_time IS NOT NULL AND
            target_entry = '08:00' AND
            entry_time >= '08:31:00';
    """)

    # set early leave
    con.sql("""
        UPDATE report
        SET is_early = 'مبكر'
        WHERE
            leave_time IS NOT NULL AND
            target_entry = '08:00' AND
            leave_time < '15:00:00';
    """)

    # attendant employees
    con.sql("""
        INSERT INTO report_present
        SELECT *
        FROM report
        WHERE
            is_early  IS NULL AND
            is_late   IS NULL AND
            is_absent IS NULL
    """)

    # drop employees that have entry & leave
    con.sql("""
        DELETE FROM report
        WHERE
            is_early  IS NULL AND
            is_late   IS NULL AND
            is_absent IS NULL
    """)
