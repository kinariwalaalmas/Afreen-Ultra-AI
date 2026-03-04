import streamlit as st
from streamlit_mic_recorder import mic_recorder

def render_sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/bubbles/100/female-profile.png") # Afreen Avatar
        st.title("👸 Afreen Pro")
        st.divider()
        st.write("👤 **Jaan's Profile**")
        st.info("Business: Surat Clothing (Baggy/Korean)")
        st.divider()
        st.write("📊 **Market Status**")
        st.success("Nifty 50: Live ✅")

def render_plus_menu():
    with st.popover("＋"):
        st.write("### Smart Tools")
        audio = mic_recorder(start_prompt="Speak 🎤", stop_prompt="Stop 🛑", key='mic')
        st.divider()
        photo = st.file_uploader("Analyze Fabric/GSM", type=["jpg", "png", "jpeg"])
        st.divider()
        ticker = st.text_input("Stock Symbol", placeholder="RELIANCE.NS")
    return audio, photo, ticker

def render_quick_actions():
    st.write("### Jaan, aaj kya plan hai?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="action-card">👕 Surat Market Trends</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="action-card">📉 Top Stock Picks</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="action-card">🎨 Baggy Design Ideas</div>', unsafe_allow_html=True)
