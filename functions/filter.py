def filter_duty(con, target_date):
    con.sql(f"""
        DELETE FROM duty_fullday
        WHERE duty_date != '{target_date}'
    """)

    con.sql(f"""
        DELETE FROM duty_halfday
        WHERE duty_date != '{target_date}'
    """)


def filter_resttime(con, target_date):
    con.sql(f"""
        DELETE FROM rest_time
        WHERE date != '{target_date}'
    """)


def filter_restday(con, target_date):
    con.sql(f"""
        DELETE from rest_day
        WHERE
            '{target_date}'::DATE < rest_start_date::DATE OR
            '{target_date}'::DATE > rest_end_date::DATE;
    """)
