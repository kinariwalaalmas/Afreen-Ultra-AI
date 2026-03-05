import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    .stApp { background-color: #fdf2f8; }
    .stChatMessage { border-radius: 15px; border: 1px solid #fbcfe8; }
    .stButton>button { border-radius: 20px; background-color: #db2777; color: white; border: none; }
    .stTextInput>div>div>input { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)
