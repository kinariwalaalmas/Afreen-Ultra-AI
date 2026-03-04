import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* Mobile-Friendly Background */
        .stApp {
            background-color: #131314;
            color: #e3e3e3;
        }

        /* Hide default audio player */
        audio { display: none; }

        /* Plus Button (Popover) ko Chat Input ke paas laane ke liye */
        div[data-testid="stPopover"] {
            position: fixed;
            bottom: 22px;
            left: 15px;
            z-index: 1000;
        }

        div[data-testid="stPopover"] > button {
            border-radius: 50% !important;
            width: 45px !important;
            height: 45px !important;
            background-color: #1f1f20 !important;
            color: #8e918f !important;
            border: 1px solid #444746 !important;
            font-size: 24px !important;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Chat Input ko thoda right shift karna taki Plus ke liye jagah bane */
        .stChatInputContainer {
            padding-left: 60px !important;
            background-color: transparent !important;
        }

        .stChatInputContainer > div {
            background-color: #1e1f20 !important;
            border-radius: 28px !important;
            border: 1px solid #444746 !important;
        }
        </style>
    """, unsafe_allow_html=True)
