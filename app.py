import streamlit as st
import asyncio
from styles import apply_styles
from ai_engine import get_clients, generate_voice, play_audio, transcribe_audio, web_search
from ui_components import render_plus_menu, render_sidebar, render_quick_actions
from vision_logic import analyze_image
from finance_expert import get_stock_analysis

# 1. Setup
st.set_page_config(page_title="Afreen Pro", layout="wide")
apply_styles()
render_sidebar()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Clients
gemini_model, groq_client = get_clients()
GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()

# 3. Quick Actions (Gemini Style)
if not st.session_state.messages:
    render_quick_actions()

# 4. Chat Display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. Tools & Input
audio_data, photo, ticker = render_plus_menu()
user_msg = st.chat_input("Jaan, puchiye...")

# Logical processing (Voice/Photo/Ticker)
if audio_data: user_msg = transcribe_audio(groq_client, audio_data['bytes'])
if photo:
    res = analyze_image(GEMINI_KEY, photo)
    st.write(res)
    asyncio.run(generate_voice(res))
    play_audio()
if ticker:
    res = get_stock_analysis(gemini_model, ticker)
    st.write(res)
    asyncio.run(generate_voice(res))
    play_audio()

# 6. Main Chat
if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"): st.write(user_msg)
    
    with st.spinner("Afreen is typing..."):
        search_info = ""
        if "market" in user_msg.lower() or "news" in user_msg.lower():
            search_info = f"Latest Search: {web_search(user_msg)}"
            
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"You are Afreen, a professional AI girl. Address user as 'Jaan' and use MASCULINE grammar. Info: {search_info}. You are Jaan's business partner in Surat."},
                *st.session_state.messages
            ]
        )
        ans = chat_completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ans})
        with st.chat_message("assistant"): st.write(ans)
        asyncio.run(generate_voice(ans))
        play_audio()
