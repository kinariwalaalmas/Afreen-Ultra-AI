import streamlit as st
import asyncio
from styles import apply_styles
from ai_engine import get_clients, generate_voice, play_audio, transcribe_audio
from ui_components import render_plus_menu
from vision_logic import analyze_image
from finance_expert import get_stock_analysis

# 1. Setup
st.set_page_config(page_title="Afreen Ultra", page_icon="👸")
apply_styles()

# 2. Clients Initialization
try:
    gemini_model, groq_client = get_clients()
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
except Exception:
    st.error("⚠️ Jaan, please check your Secrets for API keys!")
    st.stop()

st.title("👸 Afreen")

# 3. Plus Menu (Tools)
audio_data, uploaded_photo, stock_ticker = render_plus_menu()

# 4. Input Handling
user_msg = st.chat_input("Jaan, kuch bhi puchiye...")

# Voice to Text Logic
if audio_data:
    with st.spinner("Processing voice..."):
        user_msg = transcribe_audio(groq_client, audio_data['bytes'])

# Photo Analysis Logic
if uploaded_photo:
    st.image(uploaded_photo, width=200)
    if st.button("Analyze Photo 🔍"):
        res = analyze_image(GEMINI_KEY, uploaded_photo)
        st.write(res)
        asyncio.run(generate_voice(res))
        play_audio()

# Finance Analysis Logic
if stock_ticker:
    if st.button(f"Analyze {stock_ticker} 📊"):
        res = get_stock_analysis(gemini_model, stock_ticker)
        st.write(res)
        asyncio.run(generate_voice(res))
        play_audio()

# 5. Main Chat Logic (Masculine Grammar)
if user_msg:
    st.chat_message("user").write(user_msg)
    with st.spinner("Thinking..."):
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Afreen, a sweet Hinglish girl. Always address the user as 'Jaan' and ALWAYS use MASCULINE grammar (Kaise ho, kya kar rahe ho). Help him with his clothing business in Surat and Stocks."},
                {"role": "user", "content": user_msg}
            ]
        )
        ans = chat_completion.choices[0].message.content
        st.chat_message("assistant").write(ans)
        asyncio.run(generate_voice(ans))
        play_audio()
