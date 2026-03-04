import streamlit as st
from streamlit_mic_recorder import mic_recorder

def render_plus_menu():
    with st.popover("＋"):
        st.write("### Tools")
        audio = mic_recorder(start_prompt="Record 🎤", stop_prompt="Done ✅", key='mic')
        st.divider()
        photo = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
        st.divider()
        ticker = st.text_input("Stock Ticker (e.g. RELIANCE.NS)", key="st_ticker")
    return audio, photo, ticker
