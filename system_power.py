import streamlit as st
import asyncio
from edge_tts import Communicate
import os
import base64

def keep_alive_power():
    """App ko active rakhne ke liye chhota sa logic"""
    if "alive_count" not in st.session_state:
        st.session_state.alive_count = 0
    st.session_state.alive_count += 1

async def voice_power(text):
    """Afreen ki awaaz generate karne ke liye"""
    try:
        # Female voice select karna
        voice = "hi-IN-SwaraNeural" 
        communicate = Communicate(text, voice)
        await communicate.save("speech.mp3")
    except Exception as e:
        print(f"Voice Error: {e}")

def audio_player():
    """Audio file ko auto-play karne ke liye"""
    if os.path.exists("speech.mp3"):
        with open("speech.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)
        # Bajne ke baad file delete karna taaki repeat na ho
        os.remove("speech.mp3")
