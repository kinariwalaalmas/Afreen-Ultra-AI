import streamlit as st
import asyncio
from styles import apply_styles
from ai_engine import get_clients, generate_voice, play_audio, transcribe_audio
from ui_components import render_plus_menu
from vision_logic import analyze_image
from finance_expert import get_stock_analysis

# 1. Page Config & Styles
st.set_page_config(page_title="Afreen Ultra", page_icon="👸")
apply_styles()

# 2. Setup AI Clients
try:
    gemini_model, groq_client = get_clients()
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
except Exception:
    st.error("⚠️ Beby, Secrets mein keys check karo!")
    st.stop()

st.title("👸 Afreen")

# 3. Render UI Components
audio_data, uploaded_photo, stock_ticker = render_plus_menu()

# 4. User Input Handling
user_msg = st.chat_input("Beby, mujhse baat karo...")

# Voice handle
if audio_data:
    with st.spinner("Sun rahi hoon..."):
        user_msg = transcribe_audio(groq_client, audio_data['bytes'])

# Photo handle
if uploaded_photo:
    st.image(uploaded_photo, width=150)
    if st.button("Analyze Photo 🔍"):
        with st.spinner("Afreen dekh rahi hai..."):
            res = analyze_image(GEMINI_KEY, uploaded_photo)
            st.write(res)
            asyncio.run(generate_voice(res))
            play_audio()

# Stock handle
if stock_ticker:
    if st.button(f"Analyze {stock_ticker} 📈"):
        with st.spinner(f"Scanning {stock_ticker}..."):
            fin_res = get_stock_analysis(gemini_model, stock_ticker)
            st.write(fin_res)
            asyncio.run(generate_voice(fin_res))
            play_audio()

# 5. Main Chat Logic (Masculine Grammar)
if user_msg:
    st.chat_message("user").write(user_msg)
    with st.spinner("Afreen thinking..."):
        # LINE 62 FIX: Completions call properly closed
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Afreen, a sweet Hinglish girl. ALWAYS use MASCULINE grammar (Kaise ho, kar rahe ho) for Beby. You are an expert in Surat's baggy clothing business and Stocks."},
                {"role": "user", "content": user_msg}
            ]
        )
        ans = chat_completion.choices[0].message.content
        st.chat_message("assistant").write(ans)
        asyncio.run(generate_voice(ans))
        play_audio()
