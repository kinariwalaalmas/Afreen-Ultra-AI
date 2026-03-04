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

# Keys Loading
GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
GROQ_KEY = st.secrets["GROQ_API_KEY"].strip()

genai.configure(api_key=GEMINI_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_KEY)

# --- Voice Engine ---
async def text_to_speech(text):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+25%")
    await communicate.save("response.mp3")

def play_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

st.title("👸 Afreen Chat")

# --- THE "+" ICON MENU ---
# Yahan humne popover use kiya hai jo bilkul menu ki tarah khulta hai
with st.popover("➕"):
    st.write("### Tools")
    
    # 🎤 Mic Section
    st.write("Speak to me:")
    audio_data = mic_recorder(start_prompt="Start Mic 🎤", stop_prompt="Stop 🛑", key='recorder')
    
    st.divider()
    
    # 📷 Photo Section
    st.write("Upload Photo:")
    uploaded_file = st.file_uploader("Choose a photo", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

# Placeholder for final input
user_input = st.chat_input("Beby, mujhse baat karo...")

# --- LOGIC HANDLING ---

# 1. Handle Voice Input
if audio_data:
    with st.spinner("Processing voice..."):
        transcription = groq_client.audio.transcriptions.create(
            file=("audio.wav", audio_data['bytes']),
            model="distil-whisper-large-v3-en"
        )
        user_input = transcription.text

# 2. Handle Photo Input
if uploaded_file:
    st.image(uploaded_file, width=200, caption="Selected Image")
    if st.button("Analyze Uploaded Photo 🔍"):
        with st.spinner("Afreen is looking..."):
            ans = analyze_image(GEMINI_KEY, uploaded_file)
            st.write(ans)
            asyncio.run(text_to_speech(ans))
            play_audio("response.mp3")

# 3. Handle Main Chat
if user_input:
    st.chat_message("user").write(user_input)
    with st.spinner("Thinking..."):
        chat = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Afreen, a sweet Hinglish girl. Use masculine grammar for user (Kaise ho). Talk about Surat business & stocks. Call him Beby."},
                {"role": "user", "content": user_input}
            ]
        )
        ans = chat.choices[0].message.content
        st.chat_message("assistant").write(ans)
        asyncio.run(text_to_speech(ans))
        play_audio("response.mp3")
