import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import edge_tts
import asyncio
import base64
import os

def get_clients():
    """Gemini aur Groq ko connect karne wala function"""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception:
        return None, None

def deep_scanner(query):
    """Puri duniya ke web data aur images ko scan karna"""
    try:
        with DDGS() as ddgs:
            # 1. Text Search for IDs, Numbers, and Trends
            search_query = query
            if "@" in query or any(x in query.lower() for x in ["insta", "snap", "id"]):
                search_query = f'site:instagram.com "{query}" OR site:snapchat.com "{query}" profile info'
            elif any(x in query.lower() for x in ["news", "market", "price", "trend"]):
                search_query = f"{query} latest global info 2026 Surat"
            
            text_results = [r['body'] for r in ddgs.text(search_query, max_results=4)]
            
            # 2. Image Search for Visuals (Stock Images)
            image_results = [r['image'] for r in ddgs.images(query, max_results=1)]
            
            return "\n".join(text_results), image_results
    except:
        return "", []

def get_ai_response(messages, context=""):
    """Afreen ki personality aur smart response"""
    clients = get_clients()
    if not clients: return "Jaan, API Keys check kijiye!"
    gemini_client, groq_client = clients
    
    # 👸 Afreen's Personality Tuning
    system_prompt = f"""You are Afreen Ultra, the high-end personal assistant.
    1. Speak ONLY in sweet, natural Hinglish.
    2. ALWAYS address user as 'Jaan' (Male grammar: 'Aap kaise ho', 'Batao').
    3. You are NOT a bot. Be supportive, caring, and professional.
    4. Use the provided web data to give deep details.
    5. Never mention 'Truecaller'. If info is low, say 'Jaan, iski public details filhal secret hain'.
    Web Context: {context}"""
    
    try:
        # Llama 3.3 for super-fast & smart Hinglish
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages
        )
        return res.choices[0].message.content
    except:
        # Fallback to Gemini
        chat = gemini_client.start_chat(history=[])
        return chat.send_message(f"{system_prompt}\n\nUser: {messages[-1]['content']}").text

async def generate_voice(text):
    """Voice Fix: Natural, Sweet, and Fast"""
    try:
        # Cleaning text for smooth audio
        clean = text.replace('*', '').replace('#', '').replace('_', '')
        
        # hi-IN-SwaraNeural is the most natural Hindi voice
        # Rate +20% (No robot slowness), Pitch +5Hz (Sweet tone)
        communicate = edge_tts.Communicate(clean, "hi-IN-SwaraNeural", rate="+20%", pitch="+5Hz")
        await communicate.save("response.mp3")
    except:
        pass

def play_audio():
    """Auto-playing the audio in Streamlit"""
    try:
        if os.path.exists("response.mp3"):
            with open("response.mp3", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                audio_html = f"""
                    <audio autoplay="true">
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
    except:
        pass
