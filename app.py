import streamlit as st
import asyncio
from styles import apply_styles
from ai_engine import get_clients, generate_voice, play_audio, transcribe_audio
from ui_components import render_plus_menu
from vision_logic import analyze_image

# 1. Initialize
apply_styles()
gemini_model, groq_client = get_clients()

st.title("👸 Afreen")

# 2. Render UI Components (Plus Menu)
audio_data, uploaded_photo = render_plus_menu()

# 3. Handling User Input
user_msg = st.chat_input("Beby, mujhse baat karo...")

# Voice handle
if audio_data:
    with st.spinner("Sun rahi hoon..."):
        user_msg = transcribe_audio(groq_client, audio_data['bytes'])

# Photo handle
if uploaded_photo:
    st.image(uploaded_photo, width=150)
    if st.button("Analyze Photo 🔍"):
        res = analyze_image(st.secrets["GEMINI_API_KEY"], uploaded_photo)
        st.write(res)
        asyncio.run(generate_voice(res))
        play_audio()

# Chat Logic (Masculine Grammar)
if user_msg:
    st.chat_message("user").write(user_msg)
    with st.spinner("Afreen is thinking..."):
        chat_res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Afreen, a sweet Hinglish girl. ALWAYS use MASCULINE grammar (Kaise ho, kar rahe ho) for Beby. Help him with his clothing business in Surat."},
                {"role": "user", "content": user_msg}
            ]
        ).choices[0].message.content
        
        st.chat_message("assistant").write(chat_res)
        asyncio.run(generate_voice(chat_res))
        play_audio()
