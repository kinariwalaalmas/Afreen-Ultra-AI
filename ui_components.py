import streamlit as st
from streamlit_mic_recorder import mic_recorder

def render_sidebar():
    with st.sidebar:
        st.markdown("<h1 style='text-align:center;'>👸 Afreen</h1>", unsafe_allow_html=True)
        st.success("✨ **Always Active for Jaan**")
        st.divider()
        st.write("👕 **Surat Market Expert**")

def render_plus_menu():
    with st.popover("＋ Tools"):
        st.write("🕵️‍♂️ **Deep Scan (ID/URL/Phone)**")
        id_url = st.text_input("Enter Details", placeholder="@username or URL")
        scan_btn = st.button("Start Deep Scan 🔍")
        st.divider()
        st.write("🎙️ **Voice & Media**")
        audio = mic_recorder(start_prompt="Speak 🎤", stop_prompt="Stop 🛑", key='mic')
        photo = st.file_uploader("Fabric Photo", type=["jpg", "png"])
    return id_url, scan_btn, audio, photo
