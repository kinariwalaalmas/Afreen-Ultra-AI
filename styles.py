import streamlit as st

def apply_styles():
    # Wake Lock for Continuous Listening
    st.markdown("<script>if('wakeLock' in navigator){navigator.wakeLock.request('screen');}</script>", unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(160deg, #021c1e 0%, #1a1a1a 100%); color: #e0f2f1; }
        .stChatMessage { background: rgba(255, 255, 255, 0.05) !important; border-radius: 20px !important; backdrop-filter: blur(10px); }
        div[data-testid="stPopover"] { position: fixed; bottom: 30px; left: 20px; z-index: 1000; }
        div[data-testid="stPopover"] > button {
            border-radius: 50% !important; width: 60px !important; height: 60px !important;
            background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%) !important; border: none !important;
        }
        .action-card { background: rgba(255, 255, 255, 0.04); border: 1px solid gold; border-radius: 15px; padding: 15px; text-align: center; }
        .stChatInputContainer { padding-left: 80px !important; }
        </style>
    """, unsafe_allow_html=True)
