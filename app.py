import streamlit as st
import asyncio
from styles import apply_styles
from ui_components import render_sidebar
from ai_engine import deep_scanner, get_ai_response, generate_voice, play_audio, get_news_ticker, analyze_image, speech_to_text
from streamlit_mic_recorder import mic_recorder

# 1. Page & Style Setup
st.set_page_config(page_title="Afreen Ultra Pro", layout="wide")
apply_styles()
render_sidebar()

# 2. Session State & Initial Greeting
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = "Hey Jaan! 👸 Afreen haazir hai. Bataiye, aaj Surat market mein kya naya karna hai?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})
    asyncio.run(generate_voice(welcome))

# 3. Header & News Ticker
st.title("👸 Afreen Ultra Pro")
st.markdown(f"<div style='background-color:#f0f2f6; padding:10px; border-radius:10px; margin-bottom:20px;'>📢 <b>News:</b> {get_news_ticker()}</div>", unsafe_allow_html=True)

# 4. Chat History Display
# Pehli baar greeting ka audio play karna
if len(st.session_state.messages) == 1: play_audio()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        # Agar message ke saath koi image judi ho toh use dikhana
        if "image" in m:
            st.image(m["image"], use_container_width=True)

# 5. The Easy-to-Use Bottom Input Bar  (Jaisa aapne manga!)
st.markdown("---") # Ek patli line taaki input bar alag dikhe
input_col1, input_col2, input_col3 = st.columns([1, 1, 8])

with input_col1:
    # 🎤 Mic Button (Left Side)
    audio_data = mic_recorder(start_prompt="🎙️", stop_prompt="🛑", key='main_mic', use_container_width=True)

with input_col2:
    # 📷 Image/Fashion Scan Button (Middle)
    # label_visibility="collapsed" se button ke upar ka text chup jata hai, sirf icon dikhta hai
    img_file = st.file_uploader("Upload", type=['jpg', 'png', 'jpeg'], key='img_upload', label_visibility="collapsed")

with input_col3:
    # 💬 Chat Input (Right Side)
    user_input = st.chat_input("Jaan, puchiye...", key='chat_input')

# 6. Input Handling Logic
final_query = None
image_to_analyze = None

# Agar Mic use kiya gaya
if audio_data and audio_data.get('bytes'):
    with st.spinner("Sun rahi hoon..."):
        transcript = speech_to_text(audio_data['bytes'])
        if transcript: final_query = transcript

# Agar Image upload ki gayi
elif img_file:
    image_to_analyze = img_file
    final_query = "Analyze this image" # Placeholder query

# Agar Chat input use kiya gaya
elif user_input:
    final_query = user_input

# 7. AI Response Processing
if final_query:
    # User ka message add karna
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"): st.write(final_query)

    with st.spinner("Afreen soch rahi hai..."):
        # Case 1: Image Analysis
        if image_to_analyze:
            ans = analyze_image(image_to_analyze)
            # Image ko chat history mein save karna
            st.session_state.messages.append({"role": "assistant", "content": ans, "image": image_to_analyze})
            with st.chat_message("assistant"):
                st.write(ans)
                st.image(image_to_analyze, use_container_width=True)
        
        # Case 2: Text/Voice Query
        else:
            # Deep Scan for URLs/IDs
            context, images = deep_scanner(final_query)
            ans = get_ai_response(st.session_state.messages, context)
            
            # Response mein agar koi web image mili ho toh use add karna
            msg_data = {"role": "assistant", "content": ans}
            if images: msg_data["image"] = images[0]
            
            st.session_state.messages.append(msg_data)
            with st.chat_message("assistant"):
                st.write(ans)
                if images: st.image(images[0], use_container_width=True)
        
        # Voice Generation & Playback
        asyncio.run(generate_voice(ans))
        play_audio()
