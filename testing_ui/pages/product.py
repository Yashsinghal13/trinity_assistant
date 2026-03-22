import streamlit as st
from chat_ui import render_chat

if "feedback" not in st.session_state:
    st.session_state.feedback = []
    
if not st.session_state.get("logged_in"):
    st.switch_page("login_page.py")

if st.session_state.role != "product":
    st.error("⛔ You are not authorized to access this page")
    st.stop()

st.title("📦 Product Dashboard")
render_chat(role="product")