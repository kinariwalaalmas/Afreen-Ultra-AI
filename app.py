import streamlit as st
import asyncio
from styles import apply_styles
from ai_engine import *
from streamlit_mic_recorder import mic_recorder
from streamlit_autorefresh import st_autorefresh

# 1. Config & Keep-Alive
st.set_page_config(page_title="Afreen Ultra", layout="wide")
apply_styles()
st_autorefresh(interval=30000, key="afreen_keep_alive")

# 2. Afreen's Sweet Greeting
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_text = "Hey, main Afreen hoon Jaan, aap kaise hain?" 
    st.session_state.messages.append({"role": "assistant", "content": welcome_text})
    asyncio.run(generate_voice(welcome_text))

st.title("👸 Afreen Pro")
st.markdown(f"<div style='background-color:#fff1f2; padding:10px; border-radius:10px;'>📢 {get_news_ticker()}</div>", unsafe_allow_html=True)

# 3. Chat History
if len(st.session_state.messages) == 1: play_audio()
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if "image" in m: st.image(m["image"])

# 4. 🛠️ THE BOTTOM TOOLBAR (PROFESSIONAL POSITION)
st.write("---")
# Icons row: [Mic] [Camera] [Text]
col1, col2, col3 = st.columns([1, 1, 8])

final_query = None
uploaded_img = None

with col1:
    audio = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='mic')
with col2:
    uploaded_img = st.file_uploader("📷", type=['jpg', 'png'], label_visibility="collapsed")
with col3:
    user_msg = st.chat_input("Jaan, puchiye ya command dein...")

# 5. Logic
if audio and audio.get('bytes'):
    transcript = speech_to_text(audio['bytes'])
    if transcript: final_query = transcript
elif uploaded_img:
    final_query = "Analyze this image"
elif user_msg:
    final_query = user_msg

if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"): st.write(final_query)

    with st.spinner("Processing..."):
        if uploaded_img:
            ans = analyze_image(uploaded_img)
            st.session_state.messages.append({"role": "assistant", "content": ans, "image": uploaded_img})
            with st.chat_message("assistant"):
                st.write(ans); st.image(uploaded_img)
        else:
            context, imgs = deep_scanner(final_query)
            ans = get_ai_response(st.session_state.messages, context)
            msg_data = {"role": "assistant", "content": ans}
            if imgs: msg_data["image"] = imgs[0]
            st.session_state.messages.append(msg_data)
            with st.chat_message("assistant"):
                st.write(ans)
                if imgs: st.image(imgs[0])
        
        asyncio.run(generate_voice(ans))
        play_audio()
