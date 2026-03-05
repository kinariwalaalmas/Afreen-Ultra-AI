import streamlit as st
from streamlit_mic_recorder import mic_recorder

def render_plus_menu():
    """Plus button ke andar 'Deep Scan URL' option"""
    with st.popover("＋ Tools"):
        st.write("🕵️‍♂️ **Social Media Detective**")
        profile_url = st.text_input("Profile URL (Insta/Snap)", placeholder="https://instagram.com/username")
        url_scan_btn = st.button("Deep Scan URL 🚀")
        
        st.divider()
        st.write("🎙️ **Voice & Media**")
        audio = mic_recorder(start_prompt="Speak 🎤", stop_prompt="Stop 🛑", key='mic')
        photo = st.file_uploader("Upload Image", type=["jpg", "png"])
        
    return profile_url, url_scan_btn, audio, photo
