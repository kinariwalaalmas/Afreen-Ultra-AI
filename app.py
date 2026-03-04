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

# --- 1. UI aur Theme Apply karna ---
apply_styles() # Styles.py se background aur button ka look aayega

# --- 2. API Keys Load karna (Secrets se) ---
try:
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
    GROQ_KEY = st.secrets["GROQ_API_KEY"].strip()
    # News key optional hai, agar nahi hai toh koi baat nahi
except Exception:
    st.error("⚠️ Beby, pehle Streamlit Cloud Settings -> Secrets mein keys daalo!")
    st.stop()

# Clients Setup
genai.configure(api_key=GEMINI_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_KEY)

# --- 3. Natural Voice Logic (Edge-TTS) ---
async def text_to_speech(text):
    # Swara voice ko energetic aur fast banaya hai (+25% rate)
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+25%")
    await communicate.save("response.mp3")

def get_audio_html(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
    # Hidden audio player for natural feel
    return f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'

# --- 4. Main Interface ---
st.title("👸 Afreen: Your Super-Power AI")

# Section 1: Photo Analysis (Vision)
with st.expander("📷 Photo Analyze Karein (GSM, Fabric, Sourcing)"):
    uploaded_file = st.file_uploader("Beby, koi bhi photo upload karo", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, width=300)
        if st.button("Analyze Photo 🔍"):
            with st.spinner("Afreen dekh rahi hai..."):
                img = PIL.Image.open(uploaded_file)
                prompt = "Aap ek expert clothing specialist ho. Is photo ko dekh kar Hinglish mein batayein: GSM, Fabric type, aur Surat market sourcing details. Call the user Beby."
                response = vision_model.generate_content([prompt, img])
                ans = response.text
                st.write(ans)
                asyncio.run(text_to_speech(ans))
                st.markdown(get_audio_html("response.mp3"), unsafe_allow_html=True)

# Section 2: Mic & Chat Section
st.divider()
col1, col2 = st.columns([1, 6])
with col1:
    audio_data = mic_recorder(start_prompt="🎤", stop_prompt="🛑", key='recorder')

user_input = st.chat_input("Beby, mujhse baat karo (Stocks, Business, etc.)...")

# Speech to Text using Groq Whisper
if audio_data:
    with st.spinner("Sun rahi hoon..."):
        transcription = groq_client.audio.transcriptions.create(
            file=("audio.wav", audio_data['bytes']),
            model="distil-whisper-large-v3-en"
        )
        user_input = transcription.text

# Section 3: Smart Chat Logic (Hinglish)
if user_input:
    st.chat_message("user").write(user_input)
    
    with st.spinner("Afreen soch rahi hai..."):
        # Stock detection logic
        if any(word in user_input.lower() for word in ["stock", "price", ".ns"]):
            ticker = "RELIANCE.NS" # Example logic
            data = yf.Ticker(ticker)
            price = data.info.get('currentPrice', 'N/A')
            ans = f"Beby, {ticker} ka current price abhi {price} hai. Market kafi interesting lag raha hai!"
        else:
            # Fast Chat with natural Hinglish prompt
            chat = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are Afreen, a sweet, energetic Hinglish-speaking assistant. Aap Surat baggy clothing market ki expert ho. Baat karte waqt 'Beby' kaho aur natural Hinglish use karo like 'Actually', 'Waise', 'Cool'. Short answers do."},
                    {"role": "user", "content": user_input}
                ]
            )
            ans = chat.choices[0].message.content

        st.chat_message("assistant").write(ans)
        asyncio.run(text_to_speech(ans))
        st.markdown(get_audio_html("response.mp3"), unsafe_allow_html=True)
