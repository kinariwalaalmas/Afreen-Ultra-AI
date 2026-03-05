import streamlit as st
from streamlit_mic_recorder import mic_recorder

def render_sidebar():
    with st.sidebar:
        st.markdown("### 👸 Afreen Ultra")
        st.write("✨ **Unified Brain Active**")
        st.divider()
        st.info("Expert in: Surat Baggy Clothing Market")
        st.write("📍 Market: Ring Road, Surat")

def render_plus_menu():
    with st.popover("＋"):
        st.write("### Tools")
        audio = mic_recorder(start_prompt="Record 🎤", stop_prompt="Stop 🛑", key='mic')
        st.divider()
        photo = st.file_uploader("Upload Fabric Photo", type=["jpg", "png"])
        st.divider()
        ticker = st.text_input("Stock Analysis (e.g. RELIANCE.NS)")
    return audio, photo, ticker

def render_quick_actions():
    st.write("### Jaan, aaj kya plan hai?")
    col1, col2 = st.columns(2)
    with col1: st.markdown('<div class="action-card">👕 Cloth Trends</div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="action-card">📈 Stock News</div>', unsafe_allow_html=True)
