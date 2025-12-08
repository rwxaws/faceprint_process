def extract_excuses_duty(con):
    con.sql("""
        CREATE OR REPLACE TABLE report_duty_fullday AS
        SELECT
            rp.emp_voter_num,
            rp.emp_name,
            rp.date,
            rp.unit,
            rp.entry_time,
            rp.leave_time,
            rp.target_entry,
            rp.is_late,
            rp.is_early,
            rp.is_absent,
            rp.excuse,
            dfd.id,
            dfd.num_hours,
            dfd.start_hour,
            dfd.end_hour,
            dfd.duty_date,
            dfd.status
        FROM report AS rp INNER JOIN duty_fullday dfd
        ON rp.emp_voter_num = dfd.emp_voter_num
    """)

    con.sql("""
        CREATE OR REPLACE TABLE report_duty_halfday AS
        SELECT
            rp.emp_voter_num,
            rp.emp_name,
            rp.date,
            rp.unit,
            rp.entry_time,
            rp.leave_time,
            rp.target_entry,
            rp.is_late,
            rp.is_early,
            rp.is_absent,
            rp.excuse,
            dhd.id,
            dhd.num_hours,
            dhd.start_hour,
            dhd.end_hour,
            dhd.duty_date,
            dhd.status
        FROM report AS rp INNER JOIN duty_halfday as dhd
        ON rp.emp_voter_num = dhd.emp_voter_num
        WHERE dhd.end_hour >= '15:00:00';
    """)

def extract_excuses_rest(con):
    con.sql("""
        CREATE OR REPLACE TABLE report_restday AS
        SELECT
            rp.emp_voter_num,
            rp.emp_name,
            rp.date,
            rp.unit,
            rp.entry_time,
            rp.leave_time,
            rp.target_entry,
            rp.is_late,
            rp.is_early,
            rp.is_absent,
            rp.excuse,
            rd.id,
            rd.num_rest_days,
            rd.rest_start_date,
            rd.rest_end_date,
            rd.status
        FROM report AS rp INNER JOIN rest_day as rd
        ON rp.emp_voter_num = rd.emp_voter_num;
    """)

    # TODO: fix the logic of processing this
    con.sql("""
        CREATE OR REPLACE TABLE report_resttime AS
        SELECT
            rp.emp_voter_num,
            rp.emp_name,
            rp.date,
            rp.unit,
            rp.entry_time,
            rp.leave_time,
            rp.target_entry,
            rp.is_late,
            rp.is_early,
            rp.is_absent,
            rp.excuse,
            rt.id,
            rt.num_hours,
            rt.start_hour,
            rt.end_hour,
            rt.status
        FROM report AS rp INNER JOIN rest_time as rt
        ON rp.emp_voter_num = rt.emp_voter_num;
    """)

def extract_excuses(con):
    extract_excuses_duty(con)
    extract_excuses_rest(con)

    con.sql("""
        DELETE FROM report
        WHERE emp_voter_num IN (
            SELECT emp_voter_num FROM report_duty_fullday
            UNION
            SELECT emp_voter_num FROM report_duty_halfday
            UNION
            SELECT emp_voter_num FROM report_restday
            UNION
            SELECT emp_voter_num FROM report_resttime
        );
    """)
