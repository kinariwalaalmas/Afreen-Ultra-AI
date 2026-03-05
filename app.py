import streamlit as st
import asyncio

# 1. Automatic Permission Bridge (JS Request)
# Ise sabse upar rakhna hai taaki app khulte hi mic maange
st.components.v1.html("""
<script>
    // Mic aur Camera ki permission ke liye request
    navigator.mediaDevices.getUserMedia({ audio: true, video: true })
    .then(function(stream) {
        console.log('Jaan, permission mil gayi!');
    })
    .catch(function(err) {
        console.log('Error: ' + err);
    });
</script>
""", height=0)

# 2. Importing Your Super-Powers
from ui_power import apply_ui_power, render_sidebar_power
from ai_power import ai_brain, visual_scanner, get_news_ticker, speech_to_text, deep_scanner
from system_power import keep_alive_power, voice_power, audio_player

# 3. Activation & Setup
st.set_page_config(page_title="Afreen Pro", layout="wide", initial_sidebar_state="collapsed")
apply_ui_power()        # Professional Look
render_sidebar_power()   # Business Sidebar
keep_alive_power()       # Foreground Trick

# 4. Session State & Sweet Greeting
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Aapka favorite greeting message
    greet = "Hey, main Afreen hoon Jaan, aap kaise hain?"
    st.session_state.messages.append({"role": "assistant", "content": greet})
    asyncio.run(voice_power(greet))

# 5. Live News Ticker (Top)
st.markdown(f"<div class='ticker-wrap'>📢 {get_news_ticker()}</div>", unsafe_allow_html=True)

# 6. Chat History Display
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

# Layout: Mic (1), Camera (1), Text (8)
col_mic, col_cam, col_input = st.columns([1, 1, 8])

final_query = None
uploaded_img = None

with col_mic:
    # 🎙️ Mic Icon (Left)
    audio_data = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='main_mic', use_container_width=True)

with col_cam:
    # 📷 Camera Icon (Middle)
    uploaded_img = st.file_uploader("img", type=['jpg', 'png', 'jpeg'], key='img_up', label_visibility="collapsed")

with col_input:
    # 💬 Chat Input (Right) - Pushes up with keyboard
    user_msg = st.chat_input("Jaan, puchiye ya command dein...")

# 8. Processing Logic
if audio_data and audio_data.get('bytes'):
    with st.spinner("Sun rahi hoon..."):
        transcript = speech_to_text(audio_data['bytes'])
        if transcript: final_query = transcript
elif uploaded_img:
    final_query = "Analyze this image"
elif user_msg:
    final_query = user_msg

# 9. AI Thinking & Voice Response
if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"): st.write(final_query)

    with st.spinner("Processing..."):
        if uploaded_img:
            # Image Scanner Power
            ans = visual_scanner(uploaded_img)
            st.session_state.messages.append({"role": "assistant", "content": ans, "image": uploaded_img})
            with st.chat_message("assistant"):
                st.write(ans); st.image(uploaded_img)
        else:
            # Brain & Web Search Power
            context, web_imgs = deep_scanner(final_query)
            ans = ai_brain(st.session_state.messages, context)
            msg_data = {"role": "assistant", "content": ans}
            if web_imgs: msg_data["image"] = web_imgs[0]
            st.session_state.messages.append(msg_data)
            with st.chat_message("assistant"):
                st.write(ans)
                if web_imgs: st.image(web_imgs[0])
        
        # Voice generation
        asyncio.run(voice_power(ans))
        st.rerun()
