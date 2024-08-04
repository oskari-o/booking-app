import streamlit as st
import os
import json

from google.cloud import firestore
login_elements = st.empty()


if not st.session_state.get("authenticated", False):
  with login_elements:
    container = st.container()
    with container:
      correct_password = os.getenv("ADMIN_PASSWORD")
      password = st.text_input("Enter your password:", type="password")
      login_button = st.button("Login")

  if login_button:
    if len(password) == 0:
      st.error("Please enter a password")
    elif password != correct_password:
      st.error("Incorrect password")
    elif password == correct_password:
      st.session_state["authenticated"] = True
      login_elements.empty()
    # Main admin page elements here

if st.session_state.get("authenticated", False):
  service_account_info = json.loads(os.getenv("FIREBASE_SERVICE_ACCOUNT"))

  db = firestore.Client.from_service_account_info(service_account_info)

  st.title("Booking App Admin")

  # Input form that allows creating a new booking page - title of boooking page and description
  with st.form("new_booking_page"):
    st.subheader("Create a New Booking Page")
    
    # Input for url path
    url_path = st.text_input("URL Path", placeholder="Enter the URL path for your booking page")
    
    # Input for booking page title
    title = st.text_input("Booking Page Title", placeholder="Enter the title for your booking page")
    
    # Input for booking page description
    description = st.text_area("Booking Page Description", placeholder="Enter a description for your booking page")
    
    # Define which time slots are available
    time_slots = st.multiselect("Time Slots", options=["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"])
    
    # Submit button
    submit_button = st.form_submit_button("Create Booking Page")

    if submit_button:
      if title and description and url_path:
        print("Creating new booking page")
        new_page = {
          "title": title,
          "description": description,
          "time_slots": time_slots
        }
        try:
          db.collection("booking_pages").add(new_page, url_path)
          st.success(f"New booking page '{title}' created successfully!")
        except Exception as e:
          st.error(f"Error creating booking page: {e}")
      else:
        st.error("Please fill in all fields")



