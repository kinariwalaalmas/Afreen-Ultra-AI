import streamlit as st
import google.generativeai as genai
from groq import Groq
import yfinance as yf
import edge_tts
import asyncio
import os
import base64
from streamlit_mic_recorder import mic_recorder

# --- Page Setup ---
st.set_page_config(page_title="Afreen Ultra", page_icon="👸")

# CSS to Hide Audio Player and style Mic
st.markdown("""
    <style>
    audio { display: none; }
    .stApp { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

# Keys from Secrets
GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
GROQ_KEY = st.secrets["GROQ_API_KEY"].strip()

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_KEY)

# --- Better Realistic Voice (Edge-TTS) ---
async def text_to_speech(text):
    # 'hi-IN-SwaraNeural' ek bahut hi natural female Hindi voice hai
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural")
    await communicate.save("response.mp3")

def get_audio_html(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
    return f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'

st.title("👸 Afreen: Talk to Me")

# --- MIC BUTTON ---
st.write("Mic button dabayein aur boliye:")
audio_data = mic_recorder(start_prompt="🎤 Start Speaking", stop_prompt="🛑 Stop", key='recorder')

# Input Handling (Text or Voice)
user_query = st.chat_input("Ya fir yahan type karein...")

if audio_data:
    # Voice-to-text placeholder (Abhi ke liye manual chat better hai, but mic recording save ho rahi hai)
    st.info("Beby, mic recording receive ho gayi hai! (Speech-to-text feature hum next update mein dalenge).")

if user_query:
    st.chat_message("user").write(user_query)
    
    with st.spinner("Afreen soch rahi hai..."):
        # Fast Response from Groq
        chat = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are Afreen, a sweet Hindi-speaking assistant and business expert for Korean clothes."},
                      {"role": "user", "content": user_query}]
        )
        ans = chat.choices[0].message.content
        st.chat_message("assistant").write(ans)

        # Realistic Voice Generation
        asyncio.run(text_to_speech(ans))
        st.markdown(get_audio_html("response.mp3"), unsafe_allow_html=True)
