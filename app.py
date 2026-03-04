import streamlit as st
import google.generativeai as genai
import yfinance as yf
from gtts import gTTS
import io

# Page Config
st.set_page_config(page_title="Afreen Ultra AI", page_icon="👸", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { background: linear-gradient(45deg, #00d2ff, #3a7bd5); color: white; border-radius: 20px; border: none; font-weight: bold; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e3192, #1bffff); }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for API and Mode
st.sidebar.title("👸 Afreen Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
mode = st.sidebar.selectbox("Choose Mode", ["Business Growth", "Stock & ETF Analysis", "General Chat"])

def get_voice(text):
    tts = gTTS(text=text, lang='hi')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # --- MODE 1: BUSINESS GROWTH ---
    if mode == "Business Growth":
        st.header("👔 Business Consultant Mode")
        st.subheader("Men's Korean & Baggy Clothing Specialist")
        
        query = st.text_input("Apne business ke bare mein puchiye (e.g. Surat market trends, Instagram scripts, Sourcing):")
        
        if st.button("Get Expert Advice"):
            business_prompt = f"You are a business expert for a men's Korean and baggy clothing brand based in Surat. The user wants help with: {query}. Give a detailed, professional strategy in Hindi."
            response = model.generate_content(business_prompt)
            st.write(response.text)
            st.audio(get_voice(response.text), format='audio/mp3')

    # --- MODE 2: STOCKS & ETFS ---
    elif mode == "Stock & ETF Analysis":
        st.header("💹 Financial Analyst Mode")
        symbol = st.text_input("Enter Stock/ETF Ticker (e.g. RELIANCE.NS, NIFTYBEES.NS):")
        
        if st.button("Analyze Now"):
            data = yf.Ticker(symbol)
            info = data.info
            price = info.get('currentPrice', info.get('navPrice', 'N/A'))
            
            analysis_prompt = f"Analyze this asset: {symbol} with current price {price}. Give a quick 3-point analysis in Hindi for an investor."
            response = model.generate_content(analysis_prompt)
            
            st.metric(label=f"{symbol} Current Price", value=f"{price}")
            st.write(response.text)
            st.audio(get_voice(response.text), format='audio/mp3')

    # --- MODE 3: GENERAL CHAT ---
    elif mode == "General Chat":
        st.header("💬 Chat with Afreen")
        user_msg = st.chat_input("Afreen se baate karein...")
        
        if user_msg:
            chat_prompt = f"You are Afreen, a friendly and super-intelligent AI assistant. Talk to the user in a sweet and helpful Hindi-English mix. User says: {user_msg}"
            response = model.generate_content(chat_prompt)
            st.chat_message("assistant").write(response.text)
            st.audio(get_voice(response.text), format='audio/mp3', autoplay=True)

else:
    st.warning("Please enter your Gemini API key in the sidebar to activate Afreen.")
