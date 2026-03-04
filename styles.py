import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        .stApp { background-color: #131314; color: #e3e3e3; }
        audio { display: none; }
        div[data-testid="stPopover"] { position: fixed; bottom: 25px; left: 15px; z-index: 1000; }
        div[data-testid="stPopover"] > button {
            border-radius: 50% !important; width: 45px !important; height: 45px !important;
            background-color: #1f1f20 !important; color: #8e918f !important; border: 1px solid #444746 !important;
        }
        .stChatInputContainer { padding-left: 65px !important; }
        </style>
    """, unsafe_allow_html=True)
