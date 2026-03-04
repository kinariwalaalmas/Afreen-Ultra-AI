import streamlit as st
from streamlit_mic_recorder import mic_recorder

def render_sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/bubbles/100/female-profile.png")
        st.title("👸 Afreen Pro")
        brain = st.selectbox("🧠 Afreen's Brain:", ["Llama 3.3 (Fast)", "ChatGPT (OpenAI)", "Claude 3.5 Sonnet"], index=0)
        st.divider()
        st.info("Jaan's Business: Surat Baggy Clothing")
        return brain

def render_plus_menu():
    with st.popover("＋"):
        st.write("### Smart Tools")
        audio = mic_recorder(start_prompt="Speak 🎤", stop_prompt="Stop 🛑", key='mic')
        st.divider()
        photo = st.file_uploader("Analyze Fabric/GSM", type=["jpg", "png", "jpeg"])
        st.divider()
        ticker = st.text_input("Stock Symbol (e.g. RELIANCE.NS)")
    return audio, photo, ticker

def render_quick_actions():
    st.write("### Jaan, aaj kya plan hai?")
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown('<div class="action-card">👕 Surat Trends</div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="action-card">📈 Top Stocks</div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="action-card">🎨 Design Ideas</div>', unsafe_allow_html=True)
