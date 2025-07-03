import duckdb as dd
import streamlit as st

from functions.utils import rtl_text

from functions.cleanup import (
    clean_duty,
    clean_rest,
    clean_faceprint
)

from functions.filter import (
    filter_duty,
    filter_resttime,
    filter_restday,
    filter_faceprint
)
from functions.extract_excuses import extract_excuses
from functions.tables import get_excuses, get_no_excuses


def process_files(faceprint_file, rest_files, duty_file, date):
    con = dd.connect(":memory:")
    target_date = str(date)

    clean_duty(con, duty_file)
    clean_rest(con, rest_files)
    clean_faceprint(con, faceprint_file)

    filter_duty(con, target_date)
    filter_resttime(con, target_date)
    filter_restday(con, target_date)
    filter_faceprint(con)

    extract_excuses(con)
    has_excuses = get_excuses(con)
    no_excuse = get_no_excuses(con)

    rtl_text("لديه عذر", component="h2")
    st.dataframe(has_excuses, hide_index=True)
    rtl_text("بدون عذر", component="h2")
    st.dataframe(no_excuse, hide_index=True)

rtl_text("معالجة بصمات الوجه", component="h1")
rtl_text("اختر التاريخ", component="markdown")
date = st.date_input('choose date', label_visibility="collapsed")
rtl_text("ملف بصمة الوجه", component="markdown")
faceprint_file = st.file_uploader('faceprint', type="csv", label_visibility="collapsed")
rtl_text("ملفات الاجازات والزمنيات", component="markdown")
rest_files = st.file_uploader('vacation', type="xlsx", accept_multiple_files=True, label_visibility="collapsed")
rtl_text("ملف الواجبات", component="markdown")
duty_file = st.file_uploader('duty', type="xlsx", label_visibility="collapsed")

if not all([
    faceprint_file,
    rest_files,
    duty_file
]):
    st.button("بدء المعالجة", disabled=True)
else:
    if st.button("بدء المعالجة"):
        process_files(faceprint_file, rest_files, duty_file, date)
