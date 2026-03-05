import streamlit as st
import asyncio
from styles import apply_styles
from ai_engine import *
from streamlit_mic_recorder import mic_recorder
from streamlit_autorefresh import st_autorefresh

# 1. Config & Styles
st.set_page_config(page_title="Afreen Pro", layout="wide")
apply_styles()
st_autorefresh(interval=30000, key="afreen_keep_alive")

# 2. Greeting Fix (Aapka manga hua message)
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_text = "Hey, main Afreen hoon Jaan, aap kaise hain?" 
    st.session_state.messages.append({"role": "assistant", "content": welcome_text})
    asyncio.run(generate_voice(welcome_text))

# Display Greeting Voice
if len(st.session_state.messages) == 1: play_audio()

# 3. News Ticker (Top)
st.markdown(f"<div style='background-color:#fff1f2; padding:10px; border-radius:10px; border:1px solid #fecdd3;'>📢 {get_news_ticker()}</div>", unsafe_allow_html=True)

# 4. Chat Container
chat_container = st.container()
with chat_container:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])
            if "image" in m: st.image(m["image"])

# 5. 🛠️ THE PROFESSIONAL BOTTOM BAR (Toolbar)
st.markdown("<br><br><br>", unsafe_allow_html=True) # Extra space

# Layout for Icons: [Mic] [Camera] [Text Input]
# Streamlit provides chat_input separately, so we align icons just above or next to it.
col_mic, col_cam, col_void = st.columns([1, 1, 8])

final_query = None
uploaded_img = None

with col_mic:
    audio = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic', use_container_width=True)

with col_cam:
    uploaded_img = st.file_uploader("📷", type=['jpg', 'png'], label_visibility="collapsed")

# Standard chat input (Auto-pushes with keyboard)
user_msg = st.chat_input("Jaan, puchiye ya command dein...")

# 6. Response Logic
if audio and audio.get('bytes'):
    transcript = speech_to_text(audio['bytes'])
    if transcript: final_query = transcript
elif uploaded_img:
    final_query = "Analyze this image"
elif user_msg:
    final_query = user_msg

if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query})
    with chat_container: 
        with st.chat_message("user"): st.write(final_query)

    with st.spinner("Afreen is processing..."):
        if uploaded_img:
            ans = analyze_image(uploaded_img)
            st.session_state.messages.append({"role": "assistant", "content": ans, "image": uploaded_img})
        else:
            context, imgs = deep_scanner(final_query)
            ans = get_ai_response(st.session_state.messages, context)
            msg_data = {"role": "assistant", "content": ans}
            if imgs: msg_data["image"] = imgs[0]
            st.session_state.messages.append(msg_data)
        
        # UI Refresh and Voice
        st.rerun()
