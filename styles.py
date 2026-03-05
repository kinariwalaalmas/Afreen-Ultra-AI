import streamlit as st

def apply_styles():
    # --- SCREEN WAKE LOCK (Taaki phone soye nahi) ---
    st.markdown("""
        <script>
        if ('wakeLock' in navigator) {
            navigator.wakeLock.request('screen').then(() => {
                console.log('Screen Wake Lock Active for Afreen!');
            });
        }
        </script>
    """, unsafe_allow_html=True)

    # --- PREMIUM "SAPPHIRE & GOLD" THEME ---
    st.markdown("""
        <style>
        /* Main Background - Deep Sapphire Blue Gradient */
        .stApp {
            background: linear-gradient(135deg, #0a192f 0%, #112240 100%); /* Professional Deep Blue */
            color: #e6f1ff; /* Clear White-Blue Text for Readability */
            font-family: 'Helvetica Neue', sans-serif;
        }

        /* Sidebar Premium Look */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a192f 0%, #172a45 100%);
            border-right: 1px solid rgba(100, 255, 218, 0.1); /* Subtle teal border */
        }

        /* Glassmorphism Chat Bubbles (Clean & Professional) */
        .stChatMessage {
            background: rgba(23, 42, 69, 0.7) !important; /* Semi-transparent dark blue */
            border: 1px solid rgba(100, 255, 218, 0.1) !important;
            border-radius: 18px !important;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 12px;
            color: #e6f1ff !important; /* Ensure text is clear */
        }
        /* User Bubble Accent (Jaan's Messages) */
        .stChatMessage[data-testid="user-message"] {
            background: rgba(10, 25, 47, 0.8) !important;
            border: 1px solid rgba(255, 215, 0, 0.2) !important; /* Gold border for Jaan */
        }

        /* Floating Plus Button (The Jewel) */
        div[data-testid="stPopover"] {
            position: fixed; bottom: 25px; left: 20px; z-index: 1000;
        }
        div[data-testid="stPopover"] > button {
            border-radius: 50% !important; width: 58px !important; height: 58px !important;
            /* Gold to Emerald Gradient */
            background: linear-gradient(135deg, #ffd700 0%, #00b09b 100%) !important;
            box-shadow: 0 8px 20px -5px rgba(255, 215, 0, 0.5) !important;
            border: 2px solid rgba(255, 255, 255, 0.2) !important;
            color: #0a192f !important; /* Dark icon on gold button */
            font-size: 28px !important; transition: all 0.3s ease;
        }
        div[data-testid="stPopover"] > button:hover {
            transform: scale(1.05); box-shadow: 0 12px 25px -5px rgba(255, 215, 0, 0.7) !important;
        }

        /* Chat Input Bar (Sleek) */
        .stChatInputContainer {
            padding-left: 80px !important; padding-right: 20px !important; bottom: 15px !important;
        }
        .stChatInputContainer > div {
            background-color: rgba(23, 42, 69, 0.8) !important;
            border-radius: 30px !important;
            border: 1px solid rgba(100, 255, 218, 0.2) !important;
            color: #e6f1ff !important;
        }
        .stChatInputContainer > div > div > input {
             color: #e6f1ff !important; /* Input text color */
        }

        /* Action Cards (Quick Info) */
        .action-card {
            background: rgba(23, 42, 69, 0.5);
            border: 1px solid rgba(255, 215, 0, 0.15); /* Gold border */
            border-radius: 15px; padding: 18px; text-align: center;
            transition: 0.3s; cursor: pointer; backdrop-filter: blur(5px);
        }
        .action-card:hover { background: rgba(23, 42, 69, 0.8); transform: translateY(-3px); }

        /* Scrollbar Styling */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #0a192f; }
        ::-webkit-scrollbar-thumb { background: #172a45; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #ffd700; }
        </style>
    """, unsafe_allow_html=True)
