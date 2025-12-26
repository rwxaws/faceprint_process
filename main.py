import streamlit as st

from arabic_names import page_names

pages = st.navigation(
    [
        st.Page("pages/office.py", title=page_names["office"]),
        st.Page("pages/centers.py", title=page_names["centers"]),
    ]
)

pages.run()
