import streamlit as st

def apply_styles():
    # --- SCREEN WAKE LOCK (Screen ko sone nahi dega) ---
    st.markdown("""
        <script>
        if ('wakeLock' in navigator) {
            navigator.wakeLock.request('screen').then(() => {
                console.log('Screen Wake Lock Active: Afreen is listening!');
            });
        }
        </script>
    """, unsafe_allow_html=True)

    # --- PREMIUM "SURAT DIAMOND NIGHT" THEME ---
    st.markdown("""
        <style>
        /* Main Background - Deep Emerald & Charcoal Gradient */
        .stApp {
            background: linear-gradient(160deg, #021c1e 0%, #0f292d 50%, #1a1a1a 100%);
            color: #e0f2f1; /* Soft whitish-green text */
            font-family: 'Helvetica Neue', sans-serif;
        }

        /* Sidebar Premium Look */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #011517 0%, #082024 100%);
            border-right: 1px solid rgba(255, 215, 0, 0.1); /* Gold tint border */
        }

        /* Glassmorphism Chat Bubbles (Unique & Premium) */
        .stChatMessage {
            background: rgba(2, 28, 30, 0.6) !important; /* Deep transparent green */
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 18px !important;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            margin-bottom: 12px;
        }
        /* User Bubble Accent */
        .stChatMessage[data-testid="user-message"] {
            border-color: rgba(255, 215, 0, 0.3) !important; /* Gold border for Jaan */
        }

        /* Floating Plus Button (The Jewel) */
        div[data-testid="stPopover"] {
            position: fixed; bottom: 25px; left: 20px; z-index: 1000;
        }
        div[data-testid="stPopover"] > button {
            border-radius: 50% !important; width: 58px !important; height: 58px !important;
            /* Emerald to Gold Gradient */
            background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%) !important;
            box-shadow: 0 8px 20px -5px rgba(0, 176, 155, 0.5) !important;
            border: 2px solid rgba(255, 255, 255, 0.2) !important;
            color: white !important; font-size: 28px !important; transition: all 0.3s ease;
        }
        div[data-testid="stPopover"] > button:hover {
            transform: scale(1.05); box-shadow: 0 12px 25px -5px rgba(0, 176, 155, 0.7) !important;
        }

        /* Chat Input Bar (Sleek) */
        .stChatInputContainer {
            padding-left: 80px !important; padding-right: 20px !important; bottom: 15px !important;
        }
        .stChatInputContainer > div {
            background-color: rgba(255, 255, 255, 0.07) !important;
            border-radius: 30px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important; color: white !important;
        }

        /* Action Cards (Quick Info) */
        .action-card {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 215, 0, 0.15); /* Gold border */
            border-radius: 15px; padding: 18px; text-align: center;
            transition: 0.3s; cursor: pointer; backdrop-filter: blur(5px);
        }
        .action-card:hover { background: rgba(255, 255, 255, 0.08); transform: translateY(-3px); }
        </style>
    """, unsafe_allow_html=True)
