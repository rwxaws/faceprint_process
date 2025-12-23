import streamlit as st

pages = st.navigation([
              st.Page("pages/office.py", title="مكتب ذي قار"),
              # st.Page("pages/centers.py", title="المكاتب الفرعية")
              ])

pages.run()
