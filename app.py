import streamlit as st
import asyncio

# 1. Page Configuration & Professional Look
st.set_page_config(
    page_title="Afreen Ultra Pro", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Importing Your Super-Powers
from ui_power import apply_ui_power, render_sidebar_power
from ai_power import ai_brain, visual_scanner, get_news_ticker, speech_to_text, deep_scanner
from system_power import keep_alive_power, voice_power, audio_player

# ✨ Applying UI Power & Sidebar
apply_ui_power()        
render_sidebar_power()   
keep_alive_power()       

# 3. 🎙️ Auto-Permission & Mic Activation Script
st.components.v1.html("""
<script>
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) { console.log('Mic Ready Jaan!'); })
    .catch(function(err) { console.log('Mic Error: ' + err); });
</script>
""", height=0)

# 4. ✨ AUTO-GREETING LOGIC (App kholte hi baatein)
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Afreen ka pyara swagat
    welcome_msg = "Hey Almas Jaan, main Afreen hoon. Aaj Surat ka mausam aur aapka business kaisa chal raha hai? Mujhse baatein kijiye!"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    # Voice activate karna
    asyncio.run(voice_power(welcome_msg))

# 5. Live News Ticker (Top)
st.markdown(f"<div class='ticker-wrap'>📢 {get_news_ticker()}</div>", unsafe_allow_html=True)

# 6. Chat History Display
# First time audio play karne ke liye
if len(st.session_state.messages) == 1:
    audio_player()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if "image" in m and m["image"]:
            st.image(m["image"], use_container_width=True)

# 7. 🛠️ THE PROFESSIONAL TOOLBAR (Bottom Row Layout)
st.markdown("---")
from streamlit_mic_recorder import mic_recorder

# Professional Layout: [Mic] [Camera] [Chat Input]
col_mic, col_cam, col_input = st.columns([1, 1, 8])

final_query = None
uploaded_img = None

with col_mic:
    # 🎙️ Professional Mic Icon
    audio_data = mic_recorder(
        start_prompt="🎙️", 
        stop_prompt="🛑", 
        key='main_mic', 
        use_container_width=True
    )

with col_cam:
    # 📷 Camera Icon
    uploaded_img = st.file_uploader("Scan", type=['jpg', 'png', 'jpeg'], key='img_up', label_visibility="collapsed")

with col_input:
    # 💬 Modern Chat Input (Auto-pushes with keyboard)
    user_msg = st.chat_input("Jaan, puchiye ya command dein...")

# 8. Processing Input
if audio_data and audio_data.get('bytes'):
    with st.spinner("Afreen sun rahi hai..."):
        transcript = speech_to_text(audio_data['bytes'])
        if transcript: final_query = transcript
elif uploaded_img:
    final_query = "Analyze this image"
elif user_msg:
    final_query = user_msg

# 9. AI Response & Voice Playback
if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"): st.write(final_query)

    with st.spinner("Afreen is thinking..."):
        if uploaded_img:
            ans = visual_scanner(uploaded_img)
            st.session_state.messages.append({"role": "assistant", "content": ans, "image": uploaded_img})
        else:
            context, web_imgs = deep_scanner(final_query)
            ans = ai_brain(st.session_state.messages, context)
            msg_data = {"role": "assistant", "content": ans}
            if web_imgs: msg_data["image"] = web_imgs[0]
            st.session_state.messages.append(msg_data)
        
        # 📢 Awaaz taiyar karna aur UI refresh
        asyncio.run(voice_power(ans))
        st.rerun()
