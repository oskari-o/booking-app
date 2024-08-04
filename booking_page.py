import streamlit as st
import os
import json

from google.cloud import firestore

service_account = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])

db = firestore.Client.from_service_account_info(service_account)

submitted = st.session_state.get("submitted", False)

page_id = None
try:
  page_id = st.query_params["page"]
except Exception as e:
  print(e)

if not page_id:
  st.write("Nothing to see here")

if page_id:
  page_data = st.session_state.get("page_data", None)
  if not page_data:
    try:
      page_data = db.collection("booking_pages").document(page_id).get().to_dict()
      st.session_state["page_data"] = page_data
    except Exception as e:
      st.error(e)
      st.stop()
    
  st.title(page_data["title"])
  
  booked_slot = page_data.get("booked_slot")
  if booked_slot:
    st.write(f"Thank you, your booking for {booked_slot} has been confirmed!")
    st.stop()
  
  st.write(page_data["description"])
  
  selected_slot = st.session_state.get("selected_slot", None)
  for slot in page_data["time_slots"]:
    is_selected = selected_slot == slot
    def set_selected_slot():
      st.session_state["selected_slot"] = slot
    button = st.button(slot, key=slot, on_click=set_selected_slot, disabled=is_selected or submitted)
  
  send_button = st.button("Send selection", disabled=(not selected_slot) or submitted)
  if send_button:
    try:
      db.collection("booking_pages").document(page_id).update({
        "booked_slot": selected_slot,
        "booked_timestamp": firestore.SERVER_TIMESTAMP
      })
      updated_page_data = db.collection("booking_pages").document(page_id).get().to_dict()
      st.success(f"Booking sent for {selected_slot}!")
      st.session_state["page_data"] = updated_page_data
      st.session_state["submitted"] = True
      
    except Exception as e:
      st.error(e)

  
  
