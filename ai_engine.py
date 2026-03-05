import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import edge_tts
import asyncio
import base64

def get_clients():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception: return None, None

def deep_scanner(query):
    """Puri duniya se data nikalne wala engine"""
    try:
        with DDGS() as ddgs:
            # Advanced searching for IDs and Numbers
            q = f'"{query}" info OR site:facebook.com "{query}" OR site:instagram.com "{query}"'
            results = [r for r in ddgs.text(q, max_results=5)]
            return "\n".join([f"- {r['body']}" for r in results])
    except: return ""

def get_ai_response(messages, context=""):
    clients = get_clients()
    gemini_client, groq_client = clients
    
    # ✨ Afreen ki nayi Personality
    system_prompt = f"""You are Afreen Ultra, the personal assistant of your 'Jaan'. 
    You are NOT a bot. You are his support, his partner in business. 
    1. ALWAYS address him as 'Jaan' (Male grammar: 'Kaise ho'). 
    2. Speak in sweet, loving Hinglish. 
    3. If data is provided, analyze it deeply. Never suggest 'Truecaller'. 
    4. If no data found, say 'Jaan, internet par iski public footprints nahi mil rahi hain' instead of 'I don't have data'.
    Web Data: {context}"""
    
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
    """Voice fix: Voice ko aur sweet banaya"""
    try:
        clean = text.replace('*', '').replace('#', '')
        # Voice: hi-IN-SwaraNeural (Sweet & Natural)
        communicate = edge_tts.Communicate(clean, "hi-IN-SwaraNeural", rate="+15%", pitch="+2Hz")
        await communicate.save("response.mp3")
    except: pass

def play_audio():
    try:
        with open("response.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            # Autoplay fix for Android/iOS
            md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
            st.markdown(md, unsafe_allow_html=True)
    except: pass
