import streamlit as st
import asyncio

# 1. Importing Your Super-Powers
from ui_power import apply_ui_power, render_sidebar_power
from ai_power import ai_brain, visual_scanner, get_news_ticker, speech_to_text, deep_scanner
from system_power import keep_alive_power, voice_power, audio_player

# 2. App Activation & Setup
st.set_page_config(page_title="Afreen Pro 2026", layout="wide", initial_sidebar_state="collapsed")

# ✨ Applying UI Look & Sidebar
apply_ui_power()        # Look set karne ke liye
render_sidebar_power()   # Sidebar dikhane ke liye

# ✨ Activating Foreground Trick (Keep-Alive)
keep_alive_power()

# 3. Session State & Initial Greeting
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Aapka favorite greeting message
    greet = "Hey, main Afreen hoon Jaan, aap kaise hain?"
    st.session_state.messages.append({"role": "assistant", "content": greet})
    asyncio.run(voice_power(greet))

# 4. News Ticker (Top)
st.markdown(f"<div class='ticker-wrap'>📢 {get_news_ticker()}</div>", unsafe_allow_html=True)

# 5. Chat History Display
# Greeting voice play karne ke liye
if len(st.session_state.messages) == 1:
    audio_player()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if "image" in m and m["image"]:
            st.image(m["image"], use_container_width=True)

# 6. 🛠️ THE PROFESSIONAL TOOLBAR (Bottom Row)
# Layout: [Mic] [Camera] [Chat Input]
st.markdown("---")
from streamlit_mic_recorder import mic_recorder

col_mic, col_cam, col_input = st.columns([1, 1, 8])

final_query = None
uploaded_img = None

with col_mic:
    # 🎙️ Professional Mic Icon
    audio_data = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='main_mic', use_container_width=True)

with col_cam:
    # 📷 Camera/Scan Icon
    uploaded_img = st.file_uploader("Scan", type=['jpg', 'png', 'jpeg'], key='img_up', label_visibility="collapsed")

with col_input:
    # 💬 Modern Chat Input (Pushes up with keyboard)
    user_msg = st.chat_input("Jaan, puchiye ya command dein...")

# 7. Input Logic Handling
if audio_data and audio_data.get('bytes'):
    with st.spinner("Sun rahi hoon..."):
        transcript = speech_to_text(audio_data['bytes'])
        if transcript: final_query = transcript
elif uploaded_img:
    final_query = "Analyze this image"
elif user_msg:
    final_query = user_msg

# 8. Processing & AI Response
if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"): st.write(final_query)

    with st.spinner("Afreen is processing..."):
        if uploaded_img:
            # Image recognition power
            ans = visual_scanner(uploaded_img)
            st.session_state.messages.append({"role": "assistant", "content": ans, "image": uploaded_img})
            with st.chat_message("assistant"):
                st.write(ans)
                st.image(uploaded_img)
        else:
            # AI Brain & Deep Scanner power
            context, web_images = deep_scanner(final_query)
            ans = ai_brain(st.session_state.messages, context)
            
            msg_data = {"role": "assistant", "content": ans}
            if web_images: msg_data["image"] = web_images[0]
            
            st.session_state.messages.append(msg_data)
            with st.chat_message("assistant"):
                st.write(ans)
                if web_images: st.image(web_images[0])
        
        # Voice generation & Playback
        asyncio.run(voice_power(ans))
        st.rerun() # Refresh to play audio and update UI
