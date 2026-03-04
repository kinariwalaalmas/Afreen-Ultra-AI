import streamlit as st
import google.generativeai as genai
from groq import Groq
import edge_tts
import asyncio
import base64
from streamlit_mic_recorder import mic_recorder
from styles import apply_styles
from vision_logic import analyze_image

# --- 1. UI aur Theme Apply karna ---
apply_styles() # Ye styles.py se aayega

# --- 2. Keys Load karna (Secrets se) ---
try:
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
    GROQ_KEY = st.secrets["GROQ_API_KEY"].strip()
except Exception:
    st.error("⚠️ Beby, pehle Streamlit Secrets mein Keys check karo!")
    st.stop()

# Clients Setup
groq_client = Groq(api_key=GROQ_KEY)

# --- 3. Voice Logic (Edge-TTS) ---
async def text_to_speech(text):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural")
    await communicate.save("response.mp3")

def get_audio_html(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
    return f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'

# --- 4. Main App Interface ---
st.title("👸 Afreen: Your All-in-One AI")

# Sidebar for News/Stocks (Optional check)
st.sidebar.info("Hinglish Mode: ON ✅")

# Photo Upload Section
with st.expander("📷 Photo Analyze Karein (GSM, Fabric, etc.)"):
    uploaded_file = st.file_uploader("Beby, koi bhi photo upload karo", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, width=300)
        if st.button("Analyze Photo 🔍"):
            with st.spinner("Afreen dekh rahi hai..."):
                vision_res = analyze_image(GEMINI_KEY, uploaded_file)
                st.write(vision_res)
                asyncio.run(text_to_speech(vision_res))
                st.markdown(get_audio_html("response.mp3"), unsafe_allow_html=True)

# Mic and Chat Section
st.divider()
col1, col2 = st.columns([1, 5])
with col1:
    audio_data = mic_recorder(start_prompt="🎤", stop_prompt="🛑", key='recorder')

user_input = st.chat_input("Beby, mujhse baat karo...")

# Voice to Text (Whisper)
if audio_data:
    with st.spinner("Sun rahi hoon..."):
        transcription = groq_client.audio.transcriptions.create(
            file=("audio.wav", audio_data['bytes']),
            model="distil-whisper-large-v3-en"
        )
        user_input = transcription.text

# Chat Response (Hinglish Logic)
if user_input:
    st.chat_message("user").write(user_input)
    with st.spinner("Afreen soch rahi hai..."):
        chat = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "system", 
                "content": "You are Afreen, a sweet Hinglish-speaking assistant. Help with business (Surat market), stocks, and general talk. Call the user Beby." 
            },
            {"role": "user", "content": user_input}]
        )
        ans = chat.choices[0].message.content
        st.chat_message("assistant").write(ans)
        
        asyncio.run(text_to_speech(ans))
        st.markdown(get_audio_html("response.mp3"), unsafe_allow_html=True)
