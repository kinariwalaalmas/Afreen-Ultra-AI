import streamlit as st
import google.generativeai as genai
from groq import Groq
import yfinance as yf
import edge_tts
import asyncio
import base64
import PIL.Image
from streamlit_mic_recorder import mic_recorder
from styles import apply_styles
from vision_logic import analyze_image

# --- UI Setup ---
apply_styles() # Styles.py se design aayega

# --- Keys Load karna ---
try:
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
    GROQ_KEY = st.secrets["GROQ_API_KEY"].strip()
except Exception:
    st.error("⚠️ Secrets mein keys check karein!")
    st.stop()

# Clients Setup
genai.configure(api_key=GEMINI_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_KEY)

# --- Natural Voice Logic ---
async def text_to_speech(text):
    # Fast aur realistic voice (+25% rate)
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+25%")
    await communicate.save("response.mp3")

def get_audio_html(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
    return f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'

st.title("👸 Afreen Ultra: Your Powerhouse")

# --- Section: Photo Analysis ---
with st.expander("📷 Photo Analysis (GSM, Fabric, Sourcing)"):
    uploaded_file = st.file_uploader("Beby, photo upload karo", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, width=300)
        if st.button("Analyze 🔍"):
            with st.spinner("Afreen dekh rahi hai..."):
                res = analyze_image(GEMINI_KEY, uploaded_file)
                st.write(res)
                asyncio.run(text_to_speech(res))
                st.markdown(get_audio_html("response.mp3"), unsafe_allow_html=True)

st.divider()

# --- Section: Mic & Chat ---
col1, col2 = st.columns([1, 6])
with col1:
    audio_data = mic_recorder(start_prompt="🎤", stop_prompt="🛑", key='recorder')

user_input = st.chat_input("Beby, puchiye...")

if audio_data:
    with st.spinner("Sun rahi hoon..."):
        transcription = groq_client.audio.transcriptions.create(
            file=("audio.wav", audio_data['bytes']),
            model="distil-whisper-large-v3-en"
        )
        user_input = transcription.text

if user_input:
    st.chat_message("user").write(user_input)
    with st.spinner("Afreen thinking..."):
        # Correct Grammar & Hinglish Logic
        chat = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Afreen, a sweet Hinglish girl. Address the user as 'Beby' and ALWAYS use MASCULINE grammar (e.g., 'Kaise ho?', 'Kya kar rahe ho?'). Help with Surat baggy clothes and stocks. Be energetic!"},
                {"role": "user", "content": user_input}
            ]
        )
        ans = chat.choices[0].message.content
        st.chat_message("assistant").write(ans)
        asyncio.run(text_to_speech(ans))
        st.markdown(get_audio_html("response.mp3"), unsafe_allow_html=True)
