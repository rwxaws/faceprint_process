import streamlit as st
import json

def read_json_data(json_file_path):
    with open(json_file_path, "r", encoding='utf-8') as file:
        data = json.load(file)

    return data

def rtl_text(text, component="markdown"):
    rtl_style = 'style="direction:rtl; text-align: right"'
    rtl_style_center = 'style="direction:rtl; text-align: center"'

    if component == "markdown":
        st.markdown(f'<div {rtl_style}>{text}</div>', unsafe_allow_html=True)
    elif component == "h1":
        st.markdown(f'<h1 {rtl_style_center}>{text}</h1>', unsafe_allow_html=True)
    elif component == "h2":
        st.markdown(f'<h2 {rtl_style_center}>{text}</h2>', unsafe_allow_html=True)
