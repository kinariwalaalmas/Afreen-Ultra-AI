import streamlit as st

def apply_ui_power():
    """Green Mic Visibility aur Professional Layout Fix"""
    st.markdown("""
    <style>
    .stApp { background-color: #fdf2f8; }
    header, footer {visibility: hidden;}
    
    /* 🟢 GREEN MIC FIX - Sabse upar dikhne ke liye */
    button[aria-label="🎙️"] {
        background-color: #25D366 !important;
        border-radius: 50% !important;
        width: 55px !important;
        height: 55px !important;
        color: white !important;
        border: 3px solid white !important;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4) !important;
        font-size: 24px !important;
    }

    /* ➕ PLUS BUTTON */
    .stPopover button {
        background-color: #db2777 !important;
        color: white !important;
        border-radius: 50% !important;
        font-size: 22px !important;
    }

    /* Chat Bubbles */
    .stChatMessage { border-radius: 18px; margin-bottom: 10px; }
    
    /* Search Bar inside Popover Styling */
    .stTextInput input {
        border-radius: 20px !important;
        border: 1px solid #db2777 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_power():
    with st.sidebar:
        st.markdown("<h2 style='color: #db2777;'>👸 Afreen Pro</h2>", unsafe_allow_html=True)
        st.info("Owner: **Almas Shaikh**")
