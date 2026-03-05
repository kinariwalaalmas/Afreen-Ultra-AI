import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import edge_tts
import asyncio
import base64

def get_clients():
    """Gemini aur Groq ko sahi se connect karna"""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception: return None, None

def osint_scanner(query):
    """Instagram, Snapchat, Phone aur Global News dhoondhne wala engine"""
    try:
        with DDGS() as ddgs:
            # Special queries for social media and phone numbers
            search_query = query
            if "@" in query:
                search_query = f'site:instagram.com "{query}" OR site:snapchat.com "{query}"'
            elif any(x in query.lower() for x in ["news", "market", "batao", "price"]):
                search_query = f"{query} latest global info 2026"
            
            results = [r for r in ddgs.text(search_query, max_results=3)]
            return "\n".join([f"Info: {r['body']}" for r in results])
    except: return "Jaan, internet thoda slow hai, details nahi mil payi."

def get_ai_response(messages, context=""):
    """Duniya ki jankari ko analyze karke jawab dena"""
    clients = get_clients()
    if not clients: return "Jaan, API Keys missing hain!"
    gemini_client, groq_client = clients
    
    system_prompt = f"You are Afreen Ultra. Address user as 'Jaan' (Male). Use context: {context}"
    
    try:
        # Llama 3.3 for smart & fast thinking
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
    clean = text.replace('*', '').replace('#', '')
    communicate = edge_tts.Communicate(clean, "hi-IN-SwaraNeural", rate="+20%")
    await communicate.save("response.mp3")

def play_audio():
    try:
        with open("response.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass
