import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    /* Global Background */
    .stApp { background-color: #fdf2f8; }
    
    /* Chat Message Bubbles */
    .stChatMessage { border-radius: 20px; border: 1px solid #fbcfe8; margin-bottom: 10px; }
    
    /* Professional Bottom Bar */
    [data-testid="stVerticalBlock"] > div:has(div.stChatInput) {
        position: fixed;
        bottom: 20px;
        background: white;
        padding: 10px;
        border-radius: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Hide File Uploader Default Text */
    section[data-testid="stFileUploader"] > div > button { display: none; }
    </style>
    """, unsafe_allow_html=True)
