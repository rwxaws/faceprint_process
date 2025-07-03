def extract_excuses_duty(con):
    con.sql("""
        CREATE OR REPLACE TABLE faceprint_duty_fullday AS
        SELECT
            fp.emp_voter_num,
            fp.emp_name,
            fp.date,
            fp.emp_center_num,
            fp.entry_time,
            fp.leave_time,
            fp.target_entry,
            fp.is_late,
            fp.is_early,
            fp.is_absent,
            dfd.id,
            dfd.num_hours,
            dfd.start_hour,
            dfd.end_hour,
            dfd.duty_date,
            dfd.status
        FROM faceprint AS fp INNER JOIN duty_fullday dfd
        ON fp.emp_voter_num = dfd.emp_voter_num
    """)

    con.sql("""
        CREATE OR REPLACE TABLE faceprint_duty_halfday AS
        SELECT
            fp.emp_voter_num,
            fp.emp_name,
            fp.date,
            fp.emp_center_num,
            fp.entry_time,
            fp.leave_time,
            fp.target_entry,
            fp.is_late,
            fp.is_early,
            fp.is_absent,
            dhd.id,
            dhd.num_hours,
            dhd.start_hour,
            dhd.end_hour,
            dhd.duty_date,
            dhd.status
        FROM faceprint AS fp INNER JOIN duty_halfday as dhd
        ON fp.emp_voter_num = dhd.emp_voter_num
        WHERE dhd.end_hour >= '15:00:00'
    """)

def extract_excuses_rest(con):
    con.sql("""
        CREATE OR REPLACE TABLE faceprint_restday AS
        SELECT
            fp.emp_voter_num,
            fp.emp_name,
            fp.date,
            fp.emp_center_num,
            fp.entry_time,
            fp.leave_time,
            fp.target_entry,
            fp.is_late,
            fp.is_early,
            fp.is_absent,
            rd.id,
            rd.num_rest_days,
            rd.rest_start_date,
            rd.rest_end_date,
            rd.status
        FROM faceprint AS fp INNER JOIN rest_day as rd
        ON fp.emp_voter_num = rd.emp_voter_num
    """)

    # TODO: fix the logic of processing this
    con.sql("""
        CREATE OR REPLACE TABLE faceprint_resttime AS
        SELECT
            fp.emp_voter_num,
            fp.emp_name,
            fp.date,
            fp.emp_center_num,
            fp.entry_time,
            fp.leave_time,
            fp.target_entry,
            fp.is_late,
            fp.is_early,
            fp.is_absent,
            rt.id,
            rt.num_hours,
            rt.start_hour,
            rt.end_hour,
            rt.status
        FROM faceprint AS fp INNER JOIN rest_time as rt
        ON fp.emp_voter_num = rt.emp_voter_num
    """)

def extract_excuses(con):
    extract_excuses_duty(con)
    extract_excuses_rest(con)

    con.sql("""
        DELETE FROM faceprint
        WHERE emp_voter_num IN (
            SELECT emp_voter_num FROM faceprint_duty_fullday
            UNION
            SELECT emp_voter_num FROM faceprint_duty_halfday
            UNION
            SELECT emp_voter_num FROM faceprint_restday
            UNION
            SELECT emp_voter_num FROM faceprint_resttime
        )
    """)
