import streamlit as st
import asyncio
from styles import apply_styles
from ui_components import render_sidebar
from ai_engine import (
    deep_scanner, get_ai_response, generate_voice, 
    play_audio, get_news_ticker, analyze_image, speech_to_text
)
from streamlit_mic_recorder import mic_recorder
from streamlit_autorefresh import st_autorefresh

# 1. Page Configuration & Styles
st.set_page_config(page_title="Afreen Ultra Pro", layout="wide", initial_sidebar_state="collapsed")
apply_styles()
render_sidebar()

# ✨ FOREGROUND TRICK: App ko har 30 seconds mein refresh karna taaki background mein active rahe
st_autorefresh(interval=30000, key="afreen_keep_alive")

# 2. Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = "Hey Jaan! 👸 Almas Shaikh ki Afreen haazir hai. Bataiye aaj kya command hai?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})
    asyncio.run(generate_voice(welcome))

# 3. News Ticker (Top)
st.markdown(f"<div style='background-color:#fff1f2; padding:8px; border-radius:10px; border:1px solid #fecdd3; margin-bottom:15px; color:#be123c;'>📢 <b>Live:</b> {get_news_ticker()}</div>", unsafe_allow_html=True)

# 4. Chat History Display
if len(st.session_state.messages) == 1: 
    play_audio()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if "image" in m and m["image"]:
            st.image(m["image"], use_container_width=True)

# 5. 📱 THE MASTER INPUT BAR (Icons in one row)
st.markdown("---")
# Layout: Mic (1), Image (1), Text (8)
col_mic, col_img, col_text = st.columns([1, 1, 8])

final_query = None
image_to_analyze = None

with col_mic:
    # 🎙️ Mic Icon
    audio_data = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='main_mic', use_container_width=True)

with col_img:
    # 📷 Camera/Image Icon
    img_file = st.file_uploader("Scan", type=['jpg', 'png', 'jpeg'], key='img_upload', label_visibility="collapsed")

with col_text:
    # 💬 Chat Input
    user_input = st.chat_input("Jaan, puchiye ya command dein...")

# 6. Input Logic Handling
if audio_data and audio_data.get('bytes'):
    with st.spinner("Afreen sun rahi hai..."):
        transcript = speech_to_text(audio_data['bytes'])
        if transcript:
            final_query = transcript
elif img_file:
    image_to_analyze = img_file
    final_query = "Analyze this fashion/fabric"
elif user_input:
    final_query = user_input

# 7. Processing & Response
if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"): st.write(final_query)

    with st.spinner("Afreen is working..."):
        if image_to_analyze:
            ans = analyze_image(image_to_analyze)
            st.session_state.messages.append({"role": "assistant", "content": ans, "image": image_to_analyze})
            with st.chat_message("assistant"):
                st.write(ans)
                st.image(image_to_analyze, use_container_width=True)
        else:
            context, web_images = deep_scanner(final_query)
            ans = get_ai_response(st.session_state.messages, context)
            
            msg_data = {"role": "assistant", "content": ans}
            if web_images: msg_data["image"] = web_images[0]
            
            st.session_state.messages.append(msg_data)
            with st.chat_message("assistant"):
                st.write(ans)
                if web_images: st.image(web_images[0], use_container_width=True)

        asyncio.run(generate_voice(ans))
        play_audio()
