import streamlit as st
import bcrypt

def hash_password(plain_password: str) -> bytes:
    """Generate bcrypt hash from plain password"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed

# print(hash_password("dev@userprod"))
print(hash_password("product_team@123"))
