import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* Modern Background */
        .stApp {
            background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
            color: #ffffff;
        }
        
        /* Hide default audio player */
        audio { display: none; }

        /* Popover (Plus Menu) Styling */
        div[data-testid="stPopover"] > button {
            border-radius: 50% !important;
            width: 50px !important;
            height: 50px !important;
            background-color: #4f46e5 !important;
            color: white !important;
            font-size: 24px !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        }

        /* Chat Message Bubbles */
        .stChatMessage {
            border-radius: 15px !important;
            padding: 10px !important;
            margin-bottom: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)
