import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
        /* Professional Buttons */
        div.stButton > button:first-child {
            background-color: #ff4b4b;
            color: white;
            border-radius: 10px;
            border: none;
            height: 3em;
            width: 100%;
            font-weight: bold;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #ff2b2b;
            transform: scale(1.02);
        }
        /* Hide Audio Player */
        audio { display: none; }
        </style>
    """, unsafe_allow_html=True)
