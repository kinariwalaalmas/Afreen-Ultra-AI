import streamlit as st
import asyncio

# 1. Page Config
st.set_page_config(page_title="Afreen Ultra Pro", layout="wide", initial_sidebar_state="collapsed")

# 2. Imports
from ui_power import apply_ui_power, render_sidebar_power
from ai_power import ai_brain, visual_scanner, get_news_ticker, speech_to_text, deep_scanner
from system_power import keep_alive_power, voice_power, audio_player

apply_ui_power()
render_sidebar_power()
keep_alive_power()

# --- 🛠️ AUTO-MIC & LOOP FIX LOGIC ---

# Flag set karna taaki greeting sirf ek baar ho
if "greeted" not in st.session_state:
    st.session_state.greeted = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# ✨ 1. Only Greet Once (Loop Fix)
if not st.session_state.greeted:
    welcome_msg = "Hey Almas Jaan, main Afreen hoon. Bataiye aaj kya command hai?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    asyncio.run(voice_power(welcome_msg))
    st.session_state.greeted = True # Ise true karte hi loop ruk jayega

# ✨ 2. Auto-Mic Focus (Browser Trigger)
# Ye script app load hote hi mic button ko 'focus' karega
st.components.v1.html("""
<script>
    window.parent.document.addEventListener('DOMContentLoaded', function() {
        const micBtn = window.parent.document.querySelector('button[aria-label="🎙️"]');
        if (micBtn) {
            micBtn.style.border = "2px solid #db2777";
            micBtn.focus();
        }
    });
</script>
""", height=0)

# --- UI DISPLAY ---
st.title("👸 Afreen Pro")
st.markdown(f"<div class='ticker-wrap'>📢 {get_news_ticker()}</div>", unsafe_allow_html=True)

audio_player()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if "image" in m: st.image(m["image"])

# --- TOOLBAR ---
st.markdown("---")
from streamlit_mic_recorder import mic_recorder

col_mic, col_cam, col_input = st.columns([1, 1, 8])

final_query = None

with col_mic:
    # Mic ready with auto-focus
    audio_data = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='main_mic', use_container_width=True)

with col_cam:
    uploaded_img = st.file_uploader("Scan", type=['jpg', 'png', 'jpeg'], key='img_up', label_visibility="collapsed")

with col_input:
    user_msg = st.chat_input("Jaan, puchiye...")

# Logic Handling
if audio_data and audio_data.get('bytes'):
    with st.spinner("Listening..."):
        transcript = speech_to_text(audio_data['bytes'])
        if transcript: final_query = transcript
elif uploaded_img:
    final_query = "Analyze this image"
elif user_msg:
    final_query = user_msg

if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.spinner("Processing..."):
        if uploaded_img:
            ans = visual_scanner(uploaded_img)
            st.session_state.messages.append({"role": "assistant", "content": ans, "image": uploaded_img})
        else:
            context, web_imgs = deep_scanner(final_query)
            ans = ai_brain(st.session_state.messages, context)
            msg_data = {"role": "assistant", "content": ans}
            if web_imgs: msg_data["image"] = web_imgs[0]
            st.session_state.messages.append(msg_data)
        
        asyncio.run(voice_power(ans))
        st.rerun() # Refresh with new content
