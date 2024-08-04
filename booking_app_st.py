import streamlit as st
  
pages = [
  st.Page("booking_app_admin.py", title="Admin", url_path="admin"),
  st.Page("booking_page.py", title="Booking", url_path="booking"),
]

pg = st.navigation(pages)

pg.run()