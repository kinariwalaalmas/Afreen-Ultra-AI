import streamlit as st
import edge_tts
import base64
import os
from streamlit_autorefresh import st_autorefresh

def keep_alive_power():
    """Foreground Trick to keep app active"""
    st_autorefresh(interval=30000, key="afreen_heartbeat")

async def voice_power(text):
    """Natural Swara Voice Generation"""
    clean = text.replace('*', '').replace('#', '')
    communicate = edge_tts.Communicate(clean, "hi-IN-SwaraNeural", rate="+20%")
    await communicate.save("response.mp3")

def audio_player():
    if os.path.exists("response.mp3"):
        with open("response.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
