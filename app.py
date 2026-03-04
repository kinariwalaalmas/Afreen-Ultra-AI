import streamlit as st
import asyncio
from styles import apply_styles
from ai_engine import get_clients, generate_voice, play_audio, transcribe_audio
from ui_components import render_plus_menu
from vision_logic import analyze_image
from finance_expert import get_stock_analysis

# 1. Page Setup & Styling
st.set_page_config(page_title="Afreen Ultra", page_icon="👸", layout="centered")
apply_styles() # Styles.py se Gemini-style UI aayega

# 2. Initialize AI Clients (Secrets se)
try:
    gemini_model, groq_client = get_clients()
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
except Exception:
    st.error("⚠️ Beby, please check your API Keys in Streamlit Secrets!")
    st.stop()

st.title("👸 Afreen")

# 3. Render the "+" Menu (Tools)
# Ye menu Mic, Photo aur Stock Ticker return karega
audio_data, uploaded_photo, stock_ticker = render_plus_menu()

# 4. Handle Chat Input
user_msg = st.chat_input("Beby, mujhse baat karo...")

# --- LOGIC HANDLING ---

# A. Voice to Text (Whisper)
if audio_data:
    with st.spinner("Sun rahi hoon..."):
        user_msg = transcribe_audio(groq_client, audio_data['bytes'])

# B. Photo Analysis
if uploaded_photo:
    st.image(uploaded_photo, width=200, caption="Uploaded Image")
    if st.button("Analyze Photo 🔍"):
        with st.spinner("Afreen dekh rahi hai..."):
            res = analyze_image(GEMINI_KEY, uploaded_photo)
            st.write(res)
            asyncio.run(generate_voice(res)) #
            play_audio()

# C. Finance/Stock Analysis
if stock_ticker:
    if st.button(f"Analyze {stock_ticker} 📊"):
        with st.spinner(f"{stock_ticker} ki reports check kar rahi hoon..."):
            finance_res = get_stock_analysis(gemini_model, stock_ticker)
            st.write(finance_res)
            asyncio.run(generate_voice(finance_res)) #
            play_audio()

# D. Main Chat Logic (Hinglish + Masculine Grammar)
if user_msg:
    st.chat_message("user").write(user_msg)
    
    with st.spinner("Afreen thinking..."):
        # Super fast response from Groq
        chat_completion = groq_client.chat.
