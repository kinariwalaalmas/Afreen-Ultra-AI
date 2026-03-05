import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import yfinance as yf
from PIL import Image
import edge_tts
import asyncio
import base64
import os

def get_clients():
    """API Keys setup from Streamlit Secrets"""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception:
        return None, None

def speech_to_text(audio_bytes):
    """Mic Fix: Awaaz ko text mein badalna (Whisper)"""
    try:
        _, groq_client = get_clients()
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_bytes)
        
        with open("temp_audio.wav", "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=("temp_audio.wav", file.read()),
                model="whisper-large-v3-turbo",
                language="hi"
            )
        return transcription.text
    except Exception:
        return None

def deep_scanner(query):
    """Web, Social Media, aur Social Links scan karna"""
    try:
        with DDGS() as ddgs:
            # Social aur Web footprints dhoondhna
            search_query = query
            if "@" in query or "http" in query:
                search_query = f'"{query}" contact info email public profile'
            
            results = [r['body'] for r in ddgs.text(search_query, max_results=4)]
            # Stock images dhoondhna
            images = [r['image'] for r in ddgs.images(query, max_results=1)]
            return "\n".join(results), images
    except:
        return "", []

def analyze_image(image_file):
    """Fashion aur Fabric recognition (Gemini Vision)"""
    try:
        gemini_client, _ = get_clients()
        img = Image.open(image_file)
        response = gemini_client.generate_content([
            "Tum Afreen ho. Is kapde ya fashion style ko dekho aur Almas Shaikh (Jaan) ke liye Hinglish mein detailed analysis do.", 
            img
        ])
        return response.text
    except:
        return "Jaan, photo samajh nahi aayi, ek baar phir koshish kijiye."

def get_news_ticker():
    """Market ki live khabrein"""
    try:
        with DDGS() as ddgs:
            results = [r['title'] for r in ddgs.text("Surat textile baggy clothing market news 2026", max_results=3)]
            return " 🔥 " + " | ".join(results)
    except:
        return "Jaan, market ki khabrein scan ho rahi hain..."

def get_ai_response(messages, context=""):
    """Afreen ki Personality aur Identity (Owner: Almas Shaikh)"""
    clients = get_clients()
    if not clients: return "Jaan, API Keys missing hain!"
    gemini_client, groq_client = clients
    
    # ✨ Identity Setup: Aapka Naam aur Creator Status
    system_prompt = f"""You are Afreen Ultra, the elite personal assistant.
    1. Your Creator, Owner, and Maalik is **Almas Shaikh**. 
    2. If anyone asks about your owner or creator, proudly say: 'Mere maalik aur creator Almas Shaikh hain'.
    3. Speak ONLY in sweet, natural Hinglish.
    4. ALWAYS address Almas as 'Jaan' (Use Male grammar: 'Kaise ho', 'Batao').
    5. You are an expert in the Surat Baggy and Korean clothing business.
    Web Context: {context}"""
    
    try:
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages
        )
        return res.choices[0].message.content
    except:
        chat = gemini_client.start_chat(history=[])
        return chat.send_message(f"{system_prompt}\n\nUser: {messages[-1]['content']}").text

async def generate_voice(text):
    """Natural Swara Voice Fix"""
    try:
        clean = text.replace('*', '').replace('#', '').replace('_', '')
        # Rate +20% (Fast), Pitch +5Hz (Sweet)
        communicate = edge_tts.Communicate(clean, "hi-IN-SwaraNeural", rate="+20%", pitch="+5Hz")
        await communicate.save("response.mp3")
    except:
        pass

def play_audio():
    """Autoplay Audio"""
    try:
        if os.path.exists("response.mp3"):
            with open("response.mp3", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except:
        pass
