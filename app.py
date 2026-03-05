import streamlit as st
import asyncio

# 1. Page Config
st.set_page_config(page_title="Afreen Ultra", layout="wide")

# 2. Imports
from ui_power import apply_ui_power, render_sidebar_power
from ai_power import ai_brain, visual_scanner, get_news_ticker, speech_to_text, deep_scanner
from system_power import keep_alive_power, voice_power, audio_player

apply_ui_power()
render_sidebar_power()
keep_alive_power()

# --- 🛠️ SESSION & LOOP FIX ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Greeting sirf ek baar (Session State check)
    welcome = "Hey Almas Jaan, main Afreen hoon. Aaj aapka business kaisa chal raha hai?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})
    asyncio.run(voice_power(welcome))
    st.rerun() # Pehla message setup karke refresh

# --- 🎙️ AUTO-FOCUS MIC SCRIPT ---
st.components.v1.html("""
<script>
    // Mic button ko active aur chamakta hua banane ke liye
    const mic = window.parent.document.querySelector('button[aria-label="🎙️"]');
    if(mic) {
        mic.focus();
        mic.style.boxShadow = "0 0 15px #db2777";
    }
</script>
""", height=0)

# --- UI DISPLAY ---
audio_player()
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

# --- TOOLBAR ---
st.markdown("---")
from streamlit_mic_recorder import mic_recorder
col1, col2, col3 = st.columns([1, 1, 8])

final_query = None
with col1:
    audio = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='main_mic', use_container_width=True)
with col2:
    img = st.file_uploader("📷", type=['jpg', 'png'], label_visibility="collapsed")
with col3:
    user_input = st.chat_input("Jaan, puchiye...")

# Logic Handling
if audio and audio.get('bytes'):
    transcript = speech_to_text(audio['bytes'])
    if transcript: final_query = transcript
elif img:
    final_query = "Analyze image"
elif user_input:
    final_query = user_input

if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.spinner("Afreen is working..."):
        if img:
            ans = visual_scanner(img)
            st.session_state.messages.append({"role": "assistant", "content": ans, "image": img})
        else:
            context, _ = deep_scanner(final_query)
            ans = ai_brain(st.session_state.messages, context)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        
        asyncio.run(voice_power(ans))
        st.rerun()
