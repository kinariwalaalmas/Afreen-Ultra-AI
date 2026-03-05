import streamlit as st
import asyncio

# 1. Page Config & Share Fix
st.set_page_config(
    page_title="Afreen Ultra Pro", 
    layout="wide", 
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Afreen Ultra Pro - Created by Almas Shaikh (Surat)"
    }
)

# 2. Importing Your Super-Powers
from ui_power import apply_ui_power, render_sidebar_power
# ✨ Naya function import karna
from ai_power import ai_brain, visual_scanner, get_news_ticker, speech_to_text, deep_scanner, pinterest_fashion_search
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
    welcome_msg = "Hey Almas Jaan, main Afreen hoon. Aaj Surat ka mausam aur aapka business kaisa chal raha hai? Mujhse baatein kijiye!"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    asyncio.run(voice_power(welcome_msg))

# 5. Live News Ticker (Top)
st.markdown(f"<div class='ticker-wrap'>📢 {get_news_ticker()}</div>", unsafe_allow_html=True)

# 6. Chat History Display
if len(st.session_state.messages) == 1:
    audio_player()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        # Pinterest images display karna
        if "pinterest_images" in m and m["pinterest_images"]:
            # 3 columns mein images dikhana
            cols = st.columns(3)
            for i, img_url in enumerate(m["pinterest_images"]):
                with cols[i]:
                    st.image(img_url, use_container_width=True)
        # User ki uploaded image display karna
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
    audio_data = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='main_mic', use_container_width=True)

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
            # Image recognition power
            ans = visual_scanner(uploaded_img)
            st.session_state.messages.append({"role": "assistant", "content": ans, "image": uploaded_img})
            with st.chat_message("assistant"):
                st.write(ans)
                st.image(uploaded_img)
        else:
            # ✨ PINTEREST & WEB SEARCH LOGIC
            pinterest_images = []
            web_context = ""
            
            # Check agar fashion related sawal hai
            fashion_keywords = ["dress", "outfit", "fashion", "kapde", "design", "style"]
            if any(keyword in final_query.lower() for keyword in fashion_keywords):
                # Pinterest search karna
                pinterest_images = pinterest_fashion_search(final_query)
            else:
                # Normal web search karna (EFTs, etc.)
                web_context = deep_scanner(final_query)
            
            # AI Brain se jawab lena
            ans = ai_brain(st.session_state.messages, web_context)
            
            # Message data taiyar karna
            msg_data = {"role": "assistant", "content": ans}
            if pinterest_images:
                msg_data["pinterest_images"] = pinterest_images
            
            st.session_state.messages.append(msg_data)
            
            with st.chat_message("assistant"):
                st.write(ans)
                # Pinterest images display karna
                if pinterest_images:
                    cols = st.columns(3)
                    for i, img_url in enumerate(pinterest_images):
                        with cols[i]:
                            st.image(img_url, use_container_width=True)
        
        # 📢 Awaaz taiyar karna aur UI refresh
        asyncio.run(voice_power(ans))
        st.rerun()
