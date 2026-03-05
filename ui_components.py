import streamlit as st
from streamlit_mic_recorder import mic_recorder

def render_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>👸 Afreen Detective</h2>", unsafe_allow_html=True)
        st.info("🔍 **ID & Number Scanner Active**")
        st.divider()
        st.write("📍 **Surat Market Expert**")

def render_plus_menu():
    with st.popover("🕵️‍♂️ Scan ID/Number"):
        id_input = st.text_input("Enter @username or Phone Number")
        scan_btn = st.button("Start Scanning 🚀")
    
    with st.popover("＋ Tools"):
        audio = mic_recorder(start_prompt="Speak 🎤", stop_prompt="Stop 🛑", key='mic')
        photo = st.file_uploader("Upload Image", type=["jpg", "png"])
    return id_input, scan_btn, audio, photo
