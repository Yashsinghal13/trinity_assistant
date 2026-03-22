import streamlit as st
from chat_ui import render_chat

st.title("👨‍💻 Developer Dashboard")

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.switch_page("login_page.py")

if st.session_state.role != "developer":
    st.error("⛔ You are not authorized to access this page")
    st.stop()

st.write("Developer tools here")
render_chat(role="developer")