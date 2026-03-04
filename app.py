import streamlit as st
import google.generativeai as genai
from groq import Groq
import yfinance as yf
from gtts import gTTS
import requests
import io

st.set_page_config(page_title="Afreen Super-AI", layout="wide")

# --- Sidebar: Saare Power Keys Yahan Daalein ---
st.sidebar.title("💎 Afreen Super Power Keys")
gemini_key = st.sidebar.text_input("GEMINI_API_KEY", type="password")
groq_key = st.sidebar.text_input("GROQ_API_KEY (For Fast Chat)", type="password")
news_key = st.sidebar.text_input("NEWS_API_KEY (For Live News)", type="password")

mode = st.sidebar.radio("Chunye Mode:", ["Business & News", "Stock Analysis", "Ultra Fast Chat"])

def speak(text):
    tts = gTTS(text=text, lang='hi')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

# --- Mode 1: Business & Live News ---
if mode == "Business & News":
    st.header("📰 Business Intelligence & Live News")
    topic = st.text_input("Kiske baare mein news chahiye? (e.g., 'Surat Textile Market', 'Korean Fashion')", "Surat Clothing Market")
    
    if st.button("Get Live Updates"):
        if news_key:
            url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={news_key}"
            r = requests.get(url).json()
            articles = r.get('articles', [])[:3]
            for art in articles:
                st.write(f"📢 **{art['title']}**")
                st.caption(art['description'])
        else:
            st.warning("Pehle News API Key daalein!")

# --- Mode 3: Ultra Fast Chat (Groq Power) ---
elif mode == "Ultra Fast Chat":
    st.header("⚡ Ultra Fast Chat (Powered by Groq)")
    user_input = st.chat_input("Afreen se kuch bhi puchiye...")
    
    if user_input:
        if groq_key:
            client = Groq(api_key=groq_key)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Baat karo ek dost ki tarah Hindi mein: {user_input}"}]
            )
            ans = completion.choices[0].message.content
            st.write(ans)
            st.audio(speak(ans), format='audio/mp3', autoplay=True)
        else:
            st.info("Fast chat ke liye Groq Key daalein, varna Gemini use karein.")

# (Stock Analysis wala part pehle jaisa hi rahega...)
