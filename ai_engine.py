import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import edge_tts
import asyncio
import base64

def get_clients():
    """Teeno brains ko initialize karna aur errors handle karna"""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception as e:
        st.error(f"Jaan, API Keys mein problem hai: {e}")
        return None, None

def web_search(query):
    """DuckDuckGo se live market aur news nikalna"""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(f"{query} latest news Surat market", max_results=3)]
            return "\n".join([f"{r['title']}: {r['body']}" for r in results])
    except Exception:
        return "Search filhal thoda busy hai, Jaan."

def get_ai_response(messages, context=""):
    """Google, Groq aur DeepSeek ka smart fallback system"""
    gemini_client, groq_client = get_clients()
    system_prompt = f"You are Afreen, a sweet Hinglish AI. Address user as 'Jaan' (Male). Expertise: Surat Baggy/Korean Clothing. Context: {context}"
    
    user_query = messages[-1]["content"].lower()
    
    # 1. Complex Business Planning -> DeepSeek (via Groq)
    if any(x in user_query for x in ["plan", "business", "strategy", "detail"]):
        try:
            res = groq_client.chat.completions.create(
                model="deepseek-r1-distill-llama-70b",
                messages=[{"role": "system", "content": system_prompt}] + messages
            )
            return res.choices[0].message.content
        except: pass # Error aaye toh niche waale model par jump karega

    # 2. Fast/Smart Response -> Llama 3.3 (via Groq)
    try:
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages
        )
        return res.choices[0].message.content
    except:
        # 3. Ultimate Fallback -> Google Gemini
        try:
            chat = gemini_client.start_chat(history=[])
            response = chat.send_message(f"{system_prompt}\n\nUser: {user_query}")
            return response.text
        except:
            return "Jaan, saare dimaag thak gaye hain, thodi der baad koshish karein? ❤️"

async def generate_voice(text):
    try:
        clean_text = text.replace('*', '').replace('#', '')
        communicate = edge_tts.Communicate(clean_text, "hi-IN-SwaraNeural", rate="+20%")
        await communicate.save("response.mp3")
    except: pass

def play_audio():
    try:
        with open("response.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass
