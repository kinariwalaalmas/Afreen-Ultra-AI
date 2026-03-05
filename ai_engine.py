import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import edge_tts
import asyncio
import base64

def get_clients():
    """Afreen ke brains ko bina error ke connect karna"""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception: return None, None

def web_search(query):
    """Surat market aur news ki live info nikalna"""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(f"{query} latest news", max_results=2)]
            return "\n".join([f"{r['title']}: {r['body']}" for r in results])
    except: return ""

def get_ai_response(messages, context=""):
    """Auto-Brain-Switcher: Kabhi fail nahi hoga"""
    gemini_client, groq_client = get_clients()
    system_prompt = f"You are Afreen, a sweet Hinglish AI. User is 'Jaan' (Male). Context: {context}"
    user_query = messages[-1]["content"].lower()
    
    try:
        # Business/Planning ke liye DeepSeek use hoga
        if any(x in user_query for x in ["plan", "business", "detail", "socho"]):
            res = groq_client.chat.completions.create(
                model="deepseek-r1-distill-llama-70b",
                messages=[{"role": "system", "content": system_prompt}] + messages
            )
            return res.choices[0].message.content
        
        # Fast responses ke liye Llama 3.3 ya Gemini
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages
        )
        return res.choices[0].message.content
    except:
        # Fallback to Gemini if Groq fails
        chat = gemini_client.start_chat(history=[])
        return chat.send_message(f"{system_prompt}\n\nUser: {user_query}").text

async def generate_voice(text):
    communicate = edge_tts.Communicate(text.replace('*', ''), "hi-IN-SwaraNeural", rate="+20%")
    await communicate.save("response.mp3")

def play_audio():
    with open("response.mp3", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
