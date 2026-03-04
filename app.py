import streamlit as st
import google.generativeai as genai
from groq import Groq
import edge_tts
import asyncio
import base64
import PIL.Image
from streamlit_mic_recorder import mic_recorder
from styles import apply_styles
from vision_logic import analyze_image

# UI Initialization
apply_styles()

# Secrets Loading
GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
GROQ_KEY = st.secrets["GROQ_API_KEY"].strip()

genai.configure(api_key=GEMINI_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_KEY)

# --- Real Voice Logic ---
async def speak_now(text):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+25%")
    await communicate.save("afreen_voice.mp3")

def play_audio(file):
    with open(file, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

st.title("👸 Afreen")

# --- THE GEMINI "+" MENU ---
with st.popover("＋"):
    st.write("### Tools")
    
    # 🎤 Mic Option
    st.write("Bol kar baat karein:")
    audio_data = mic_recorder(start_prompt="Record Voice 🎤", stop_prompt="Done ✅", key='mic')
    
    st.divider()
    
    # 📷 Camera/Gallery Option
    st.write("Photo analysis:")
    photo = st.file_uploader("Upload or Capture", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

# Standard Chat Input
user_msg = st.chat_input("Beby, mujhse baat karo...")

# --- LOGIC HANDLING ---

# 1. Voice to Text (Whisper)
if audio_data:
    with st.spinner("Processing..."):
        transcription = groq_client.audio.transcriptions.create(
            file=("audio.wav", audio_data['bytes']),
            model="distil-whisper-large-v3-en"
        )
        user_msg = transcription.text

# 2. Image Analysis
if photo:
    st.image(photo, width=150)
    if st.button("Analyze this Photo 🔍"):
        with st.spinner("Afreen dekh rahi hai..."):
            res = analyze_image(GEMINI_KEY, photo)
            st.write(res)
            asyncio.run(speak_now(res))
            play_audio("afreen_voice.mp3")

# 3. Main Chat (Hinglish + Masculine)
if user_msg:
    st.chat_message("user").write(user_msg)
    with st.spinner("Thinking..."):
        chat = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Afreen, a sweet Hinglish girl. ALWAYS use masculine grammar (Kaise ho, kar rahe ho). Help Beby with his clothing business in Surat and stocks."},
                {"role": "user", "content": user_msg}
            ]
        )
        ans = chat.choices[0].message.content
        st.chat_message("assistant").write(ans)
        asyncio.run(speak_now(ans))
        play_audio("afreen_voice.mp3")
