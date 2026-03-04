import streamlit as st
from groq import Groq
import google.generativeai as genai
import edge_tts
import asyncio
import base64

def get_clients():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
    return genai.GenerativeModel('gemini-1.5-flash'), groq_client

async def generate_voice(text):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+25%")
    await communicate.save("response.mp3")

def play_audio():
    with open("response.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

def transcribe_audio(groq_client, audio_bytes):
    return groq_client.audio.transcriptions.create(
        file=("audio.wav", audio_bytes),
        model="distil-whisper-large-v3-en"
    ).text
