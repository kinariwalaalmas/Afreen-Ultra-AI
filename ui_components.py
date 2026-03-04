import streamlit as st
from streamlit_mic_recorder import mic_recorder

def render_plus_menu():
    # Gemini-style Popover Menu
    with st.popover("＋"):
        st.write("### Afreen's Tools")
        
        # Mic Option
        st.write("Bol kar baat karein:")
        audio_data = mic_recorder(start_prompt="Record 🎤", stop_prompt="Done ✅", key='mic')
        
        st.divider()
        
        # Photo Option
        st.write("Photo analysis:")
        photo = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
        
    return audio_data, photo
