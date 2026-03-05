import streamlit as st

def apply_styles():
    # --- SCREEN WAKE LOCK (Phone ko sone nahi dega) ---
    st.markdown("<script>if('wakeLock' in navigator){navigator.wakeLock.request('screen');}</script>", unsafe_allow_html=True)

    # --- "GEMINI STYLE" CLEAN LIGHT THEME ---
    st.markdown("""
        <style>
        /* 1. Main Background - Clean White */
        .stApp {
            background-color: #ffffff; /* Pure white */
            color: #212529; /* Dark grey text for best readability */
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }

        /* 2. Sidebar - Slightly off-white to separate */
        [data-testid="stSidebar"] {
            background-color: #f8f9fa; /* Very light grey */
            border-right: 1px solid #dee2e6;
        }

        /* Bold Titles like Gemini */
        h1, h2, h3 {
            color: #1a73e8 !important; /* Google-like blue for headers */
            font-weight: 700 !important; /* Extra Bold */
        }

        /* 3. Chat Bubbles - Distinct & Clean */
        .stChatMessage {
            padding: 1rem;
            border-radius: 18px !important;
            margin-bottom: 12px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05); /* Subtle shadow */
        }

        /* Assistant (Afreen) Bubble - Light Grey */
        .stChatMessage[data-testid="assistant-message"] {
            background-color: #f1f3f5 !important;
            border: 1px solid #dee2e6 !important;
            color: #212529 !important;
        }

        /* User (Jaan) Bubble - Light Blue Accent */
        .stChatMessage[data-testid="user-message"] {
            background-color: #e3f2fd !important; /* Light blue tint */
            border: none !important;
            color: #0d47a1 !important; /* Darker blue text */
        }

        /* 4. Action Cards (Quick Links) */
        .action-card {
            background-color: #ffffff;
            border: 1px solid #dfe1e5;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            color: #3c4043;
            font-weight: 600;
            box-shadow: 0 1px 3px rgba(60,64,67,0.3);
            transition: all 0.2s ease-in-out;
        }
        .action-card:hover {
            background-color: #f1f3f5;
            border-color: #1a73e8;
            transform: translateY(-3px);
        }

        /* 5. Floating Plus Button (Pop of Color) */
        div[data-testid="stPopover"] > button {
            /* Blue to Green Gradient like Google */
            background: linear-gradient(135deg, #4285f4 0%, #34a853 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(66,133,244,0.3) !important;
            width: 55px !important; height: 55px !important;
        }

        /* 6. Chat Input Box - Clean white shadow */
        .stChatInputContainer > div {
            background-color: #ffffff !important;
            border: 1px solid #dfe1e5 !important;
            border-radius: 24px !important;
            box-shadow: 0 1px 6px rgba(32,33,36,0.28) !important;
        }
        .stChatInputContainer textarea {
            color: #212529 !important; /* Dark Input text */
        }

        /* Code Blocks styling (Dark block for contrast) */
        code {
            color: #d63384; /* Pinkish hue for inline code */
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 4px;
        }
        .stCodeBlock {
            border-radius: 10px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
