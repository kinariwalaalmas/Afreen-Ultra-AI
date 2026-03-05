import streamlit as st

def apply_ui_power():
    """App ka professional look aur sticky toolbar fix"""
    st.markdown("""
    <style>
    /* Full App Theme */
    .stApp { background-color: #fdf2f8; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 🟢 Green Mic Styling */
    div[data-testid="stVerticalBlock"] > div:has(button:contains("🎙️")) button {
        background-color: #25D366 !important;
        color: white !important;
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
    }

    /* ➕ Plus Button Styling */
    .stPopover button {
        background-color: #db2777 !important;
        color: white !important;
        border-radius: 50% !important;
        font-size: 24px !important;
    }

    /* Chat Bubbles */
    .stChatMessage { border-radius: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    
    /* Sticky Bottom Container */
    [data-testid="stVerticalBlock"] > div:has(div.stChatInput) {
        position: fixed;
        bottom: 10px;
        z-index: 1000;
        background: white;
        padding: 10px;
        border-radius: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_power():
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: #db2777;'>👸 Afreen Ultra</h1>", unsafe_allow_html=True)
        st.info("Created & Owned by:\n**Almas Shaikh**")
        st.success("Business: **Surat Baggy Fashion**")
