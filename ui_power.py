import streamlit as st

def apply_ui_power():
    st.markdown("""
    <style>
    /* Professional Chat Theme */
    .stApp { background-color: #fdf2f8; }
    
    /* Sticky Bottom Toolbar Logic */
    .stChatInput {
        position: fixed;
        bottom: 10px;
        z-index: 1000;
    }
    
    /* Modern Chat Bubbles */
    .stChatMessage { 
        border-radius: 20px; 
        box-shadow: 0 2px 10px rgba(219, 39, 119, 0.1); 
    }
    
    /* News Ticker Styling */
    .ticker-wrap {
        background: white;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #fecdd3;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
