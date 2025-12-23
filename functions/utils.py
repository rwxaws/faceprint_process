import streamlit as st


def rtl_text(text, component="markdown"):
    rtl_style = 'style="direction:rtl; text-align: right"'
    rtl_style_center = 'style="direction:rtl; text-align: center"'

    if component == "markdown":
        st.markdown(f'<div {rtl_style}>{text}</div>', unsafe_allow_html=True)
    elif component == "h1":
        st.markdown(f'<h1 {rtl_style_center}>{text}</h1>',
                    unsafe_allow_html=True)
    elif component == "h2":
        st.markdown(f'<h2 {rtl_style_center}>{text}</h2>',
                    unsafe_allow_html=True)


def load_sql(filename):
    with open(f"{filename}") as f:
        return f.read()


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

