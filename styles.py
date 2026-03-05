import streamlit as st

def apply_styles():
    # Wake Lock: Screen ko sone nahi dega
    st.markdown("<script>if('wakeLock' in navigator){navigator.wakeLock.request('screen');}</script>", unsafe_allow_html=True)

    # "GEMINI STYLE" LIGHT THEME
    st.markdown("""
        <style>
        .stApp { background-color: #ffffff; color: #212529; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        [data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 1px solid #dee2e6; }
        
        /* Titles & Headings */
        h1, h2, h3 { color: #1a73e8 !important; font-weight: 700 !important; }

        /* Chat Bubbles */
        .stChatMessage { border-radius: 20px !important; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .stChatMessage[data-testid="assistant-message"] { background-color: #f1f3f4 !important; color: #212529 !important; }
        .stChatMessage[data-testid="user-message"] { background-color: #e8f0fe !important; color: #174ea6 !important; border: 1px solid #c2e7ff !important; }

        /* Action Cards */
        .action-card { background: white; border: 1px solid #dadce0; border-radius: 12px; padding: 15px; text-align: center; font-weight: 600; cursor: pointer; transition: 0.2s; }
        .action-card:hover { border-color: #1a73e8; background: #f8f9fa; transform: translateY(-2px); }

        /* Floating Plus Button */
        div[data-testid="stPopover"] > button {
            background: linear-gradient(135deg, #4285f4 0%, #34a853 100%) !important;
            border: none !important; color: white !important; width: 55px !important; height: 55px !important;
        }
        </style>
    """, unsafe_allow_html=True)
