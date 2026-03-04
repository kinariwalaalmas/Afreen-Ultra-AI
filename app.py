import streamlit as st
import google.generativeai as genai
from groq import Groq
import yfinance as yf
from gtts import gTTS
import requests
import io

# App Layout
st.set_page_config(page_title="Afreen Ultra Smart", page_icon="👸")

# Secrets se Keys uthana (with .strip() to remove accidental spaces)
try:
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip()
    GROQ_KEY = st.secrets["GROQ_API_KEY"].strip()
    NEWS_KEY = st.secrets["NEWS_API_KEY"].strip()
except Exception as e:
    st.error("⚠️ Secrets mein keys check karein!")
    st.stop()

# AI Setup
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_KEY)

def speak(text):
    tts = gTTS(text=text, lang='hi')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

st.title("👸 Afreen Super-AI")

user_query = st.chat_input("Stocks, Business ya News... kuch bhi puchiye!")

if user_query:
    st.chat_message("user").write(user_query)
    
    with st.spinner("Afreen soch rahi hai..."):
        try:
            # Smart Detection (Simple way)
            if any(word in user_query.lower() for word in ["stock", "price", "share", ".ns"]):
                # Stock Logic
                ticker = "RELIANCE.NS" # Default
                for word in user_query.upper().split():
                    if ".NS" in word: ticker = word
                data = yf.Ticker(ticker)
                price = data.info.get('currentPrice', 'N/A')
                ans = f"{ticker} ka price abhi {price} hai. Ye ek achha investment ho sakta hai."
            
            elif "news" in user_query.lower() or "khabar" in user_query.lower():
                # News Logic
                url = f"https://newsapi.org/v2/everything?q={user_query}&apiKey={NEWS_KEY}"
                r = requests.get(url).json()
                ans = f"Latest News: {r['articles'][0]['title']}" if r.get('articles') else "Abhi koi news nahi mili."

            else:
                # Fast Chat with Groq
                chat = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "You are Afreen, a business expert for Korean clothes in Surat. Answer in sweet Hindi."},
                              {"role": "user", "content": user_query}]
                )
                ans = chat.choices[0].message.content

            st.chat_message("assistant").write(ans)
            st.audio(speak(ans), format='audio/mp3', autoplay=True)

        except Exception as e:
            st.error(f"Error: {e}. Check if your API Keys are active!")
