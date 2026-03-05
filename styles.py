import streamlit as st

def apply_styles():
    # --- SCREEN WAKE LOCK (Taaki phone soye nahi) ---
    st.markdown("<script>if('wakeLock' in navigator){navigator.wakeLock.request('screen');}</script>", unsafe_allow_html=True)

    # --- PREMIUM "SAPPHIRE & GOLD" THEME ---
    st.markdown("""
        <style>
        /* Main Background - Deep Sapphire Blue */
        .stApp {
            background: linear-gradient(135deg, #0a192f 0%, #112240 100%);
            color: #e6f1ff; /* Bright readable text */
            font-family: 'Helvetica Neue', sans-serif;
        }

        /* Sidebar Look */
        [data-testid="stSidebar"] {
            background: #0a192f !important;
            border-right: 1px solid rgba(255, 215, 0, 0.2);
        }

        /* Chat Bubbles (Clean & Professional) */
        .stChatMessage {
            background: rgba(23, 42, 69, 0.8) !important;
            border: 1px solid rgba(100, 255, 218, 0.1) !important;
            border-radius: 15px !important;
            color: #ffffff !important;
            margin-bottom: 15px;
        }
        
        /* User Bubble (Jaan's Message) */
        .stChatMessage[data-testid="user-message"] {
            border: 1px solid gold !important;
            background: rgba(10, 25, 47, 0.9) !important;
        }

        /* Action Cards (Premium Gold Borders) */
        .action-card {
            background: rgba(23, 42, 69, 0.6);
            border: 2px solid #ffd700;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            color: #ffd700;
            font-weight: bold;
            transition: 0.3s;
        }
        .action-card:hover { 
            background: #ffd700; 
            color: #0a192f; 
            transform: translateY(-5px); 
        }

        /* Input Bar */
        .stChatInputContainer > div {
            background-color: #172a45 !important;
            border: 1px solid #ffd700 !important;
            border-radius: 25px !important;
        }
        </style>
    """, unsafe_allow_html=True)
