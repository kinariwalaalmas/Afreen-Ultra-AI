import streamlit as st
import asyncio
from styles import apply_styles
from ai_engine import get_clients, generate_voice, play_audio, transcribe_audio, web_search
from ui_components import render_plus_menu
from vision_logic import analyze_image
from finance_expert import get_stock_analysis

# 1. Page Config & State
st.set_page_config(page_title="Afreen Ultra", page_icon="👸")
apply_styles()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Clients Setup
try:
    gemini_model, groq_client = get_clients()
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
except Exception:
    st.error("⚠️ Jaan, please check your Secrets for API keys!")
    st.stop()

st.title("👸 Afreen")

# 3. Tools Menu
audio_data, uploaded_photo, stock_ticker = render_plus_menu()

# 4. User Input
user_msg = st.chat_input("Jaan, mujhse baat karo...")

# Voice handle
if audio_data:
    with st.spinner("Sun rahi hoon..."):
        user_msg = transcribe_audio(groq_client, audio_data['bytes'])

# Photo handle
if uploaded_photo:
    st.image(uploaded_photo, width=150)
    if st.button("Analyze Photo 🔍"):
        with st.spinner("Dekh rahi hoon..."):
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

# 5. Chat Logic
if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    st.chat_message("user").write(user_msg)
    
    with st.spinner("Afreen thinking..."):
        search_info = ""
        if any(x in user_msg.lower() for x in ["news", "market", "bhav"]):
            search_info = f"Search Result: {web_search(user_msg)}"
            
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"You are Afreen, a sweet Hinglish girl. Address user as 'Jaan' and use MASCULINE grammar. Info: {search_info}. Help with Surat baggy clothes and stocks."},
                *st.session_state.messages
            ]
        )
        ans = chat_completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ans})
        st.chat_message("assistant").write(ans)
        asyncio.run(generate_voice(ans))
        play_audio()
