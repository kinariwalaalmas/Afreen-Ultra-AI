import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* Modern Dark Theme */
        .stApp {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
        }

        /* Glassmorphism Chat Bubbles */
        .stChatMessage {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 20px !important;
            backdrop-filter: blur(10px);
            margin-bottom: 15px;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Plus Button Floating Effect */
        div[data-testid="stPopover"] {
            position: fixed; bottom: 30px; left: 20px; z-index: 1000;
        }
        div[data-testid="stPopover"] > button {
            border-radius: 50% !important; width: 60px !important; height: 60px !important;
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4) !important;
            border: none !important; color: white !important; font-size: 30px !important;
        }

        /* Action Cards */
        .action-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px; padding: 15px; text-align: center;
            transition: 0.3s; cursor: pointer;
        }
        .action-card:hover { background: rgba(255, 255, 255, 0.08); }
        </style>
    """, unsafe_allow_html=True)
