import streamlit as st
import google.generativeai as genai
from groq import Groq
import yfinance as yf
from gtts import gTTS
import requests
import io

# Page Config
st.set_page_config(page_title="Afreen Ultra Smart", page_icon="👸")

# API Keys from Streamlit Secrets (Baar-baar dalne ki zaroorat nahi)
try:
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    NEWS_KEY = st.secrets["NEWS_API_KEY"]
except Exception:
    st.error("⚠️ Pehle Streamlit Cloud ki settings mein 'Secrets' add karein!")
    st.stop()

# Setup AI Models
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
groq_client = Groq(api_key=GROQ_KEY)

def speak(text):
    tts = gTTS(text=text, lang='hi')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

st.title("👸 Afreen: Your Smart Assistant")
st.write("Main khud samajh jaungi aapko kya chahiye. Bas puchiye!")

user_query = st.chat_input("Mujhse kuch bhi puchiye (Stocks, Business ya News)...")

if user_query:
    st.chat_message("user").write(user_query)
    
    # --- SMART ROUTER: Afreen khud faisla karegi ---
    # Hum Gemini se puchenge ki user ka intent kya hai
    intent_prompt = f"Categorize this query into ONE word: 'STOCK', 'NEWS', 'BUSINESS', or 'CHAT'. Query: {user_query}"
    intent = model.generate_content(intent_prompt).text.strip().upper()

    with st.spinner("Afreen soch rahi hai..."):
        response_text = ""
        
        # 1. Agar Stock ke baare mein hai
        if "STOCK" in intent or ".NS" in user_query.upper():
            # Ticker extract karne ki koshish (e.g., RELIANCE.NS)
            words = user_query.split()
            ticker = next((w.upper() for w in words if ".NS" in w.upper() or len(w) <= 5), "RELIANCE.NS")
            data = yf.Ticker(ticker)
            price = data.info.get('currentPrice', 'N/A')
            response_text = f"{ticker} ka current price {price} hai. " + model.generate_content(f"Analyze {ticker} price {price} in Hindi briefly.").text

        # 2. Agar News chahiye
        elif "NEWS" in intent:
            url = f"https://newsapi.org/v2/everything?q={user_query}&apiKey={NEWS_KEY}"
            r = requests.get(url).json()
            article = r.get('articles', [{}])[0]
            response_text = f"Latest News: {article.get('title', 'Koi khabar nahi mili')}. " + article.get('description', '')

        # 3. Business ya General Chat (Groq Power)
        else:
            chat_completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "You are Afreen, a business and fashion expert for Korean baggy clothes in Surat. Answer in sweet Hindi-English."},
                          {"role": "user", "content": user_query}]
            )
            response_text = chat_completion.choices[0].message.content

        # Output Dikhana aur Bolna
        st.chat_message("assistant").write(response_text)
        st.audio(speak(response_text), format='audio/mp3', autoplay=True)
