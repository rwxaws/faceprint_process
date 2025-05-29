from pathlib import Path

import streamlit as st

from functions.utils import rtl_text, read_json_data
from functions.pre_process.faceprint.faceprint_format import format_faceprint
from functions.processing.attendant.attendant import extract_attendant
from functions.pre_process.duty.duty_processing import duty_process
from functions.pre_process.vacation.vacation_processing import vacation_process
from functions.pre_process.vacation_duty.combine import combine_vacation_duty
from functions.processing.earlylateabsent.earlylate_absent import extract_earlylate_absent
from functions.processing.excuses.excuses import extract_excuses
from functions.post_process.change_headers import change_headers


def process_files(faceprint_path, vacation_paths, duty_path, date):
    headers_path = Path(__file__).parent / 'required' / 'headers.json'

    headers = read_json_data(headers_path)
    arabic_headers = headers['post_processing']
    date           = str(date)

    faceprint_df = format_faceprint(faceprint_path, date)
    attendant_df = extract_attendant(faceprint_df, date)
    vacation_df  = vacation_process(vacation_paths, headers)
    # TODO: remove the need for the hour
    duty_df      = duty_process(duty_path, headers, 15)


    vacation_duty = combine_vacation_duty(vacation_df, duty_df)

    earlylate_absent_df = extract_earlylate_absent(faceprint_df, date)
    has_excuses, no_excuse = extract_excuses(vacation_duty, earlylate_absent_df, headers, date)
    
    has_excuses  = change_headers(has_excuses, arabic_headers['excuse'])
    no_excuse    = change_headers(no_excuse, arabic_headers['no_excuse'])
    attendant_df = change_headers(attendant_df, arabic_headers['attendant'])

    rtl_text("لديه عذر", component="h2")
    st.dataframe(has_excuses, hide_index=True)
    rtl_text("بدون عذر", component="h2")
    st.dataframe(no_excuse, hide_index=True)
    rtl_text("حضور", component="h2")
    st.dataframe(attendant_df, hide_index=True)


rtl_text("معالجة بصمات الوجه", component="h1")

rtl_text("اختر التاريخ", component="markdown")
date = st.date_input('choose date', label_visibility="collapsed")

rtl_text("ملف بصمة الوجه", component="markdown")
faceprint_file = st.file_uploader('faceprint', type="csv", label_visibility="collapsed")

rtl_text("ملفات الاجازات والزمنيات", component="markdown")
vacation_files = st.file_uploader('vacation', type="xlsx", accept_multiple_files=True, label_visibility="collapsed")

rtl_text("ملف الواجبات", component="markdown")
duty_file = st.file_uploader('duty', type="xlsx", label_visibility="collapsed")

if not all([
    faceprint_file,
    vacation_files,
    duty_file
]):
    st.button("بدء المعالجة", disabled=True)
else:
    if st.button("بدء المعالجة"):
        process_files(faceprint_file, vacation_files, duty_file, date)
