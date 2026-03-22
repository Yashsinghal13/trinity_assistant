import streamlit as st
import bcrypt
from user_db import USER_DB

st.set_page_config(page_title="Trinity AI Assistant", page_icon="🔐")

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []

st.title("🔐 Trinity AI Login Portal")

if not st.session_state.logged_in:
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

    if login_btn:
        if username in USER_DB and verify_password(password, USER_DB[username]["password"]):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = USER_DB[username]["role"]
            st.success("✅ Login successful")
            if st.session_state.role == "developer":
                st.switch_page("pages/developer.py")
            elif st.session_state.role == "product":
                st.switch_page("pages/product.py")
        else:
            st.error("❌ Invalid credentials")
else:
    st.success(f"Welcome {st.session_state.username}")