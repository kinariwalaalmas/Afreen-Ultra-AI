import streamlit as st
from streamlit_mic_recorder import mic_recorder

def render_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>👸 Afreen Pro</h2>", unsafe_allow_html=True)
        st.success("✨ **Always Active for Jaan**")
        st.divider()
        st.write("👕 **Surat Market Expert**")

def render_plus_menu():
    """Simple tools for scanning IDs and media"""
    with st.popover("＋ Tools"):
        id_input = st.text_input("Enter ID or Number", placeholder="@username or 98765...")
        scan_btn = st.button("Deep Scan 🔍")
        st.divider()
        audio = mic_recorder(start_prompt="Speak 🎤", stop_prompt="Stop 🛑", key='mic')
        photo = st.file_uploader("Upload Image", type=["jpg", "png"])
    return id_input, scan_btn, audio, photo
