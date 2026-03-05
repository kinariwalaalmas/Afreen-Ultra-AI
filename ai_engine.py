import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import edge_tts
import asyncio
import base64

def get_clients():
    """Sirf stable clients: Google aur Groq"""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception as e:
        st.error(f"Jaan, API Keys check kijiye: {e}")
        return None, None

def web_search(query):
    """DuckDuckGo se live market aur news info"""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(f"{query} Surat market trends", max_results=2)]
            return "\n".join([f"{r['title']}: {r['body']}" for r in results])
    except: return ""

def get_ai_response(messages, context=""):
    """Auto-routing: Groq (Fast) + Gemini (Fallback)"""
    gemini_client, groq_client = get_clients()
    system_prompt = f"You are Afreen, a sweet Hinglish AI. Address user as 'Jaan' (Male). Context: {context}"
    
    try:
        # Groq (Llama 3.3) - Ye DeepSeek se 10x fast hai
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages
        )
        return res.choices[0].message.content
    except:
        # Fallback to Google Gemini (Aankhon ke liye best)
        try:
            chat = gemini_client.start_chat(history=[])
            return chat.send_message(f"{system_prompt}\n\nUser: {messages[-1]['content']}").text
        except:
            return "Jaan, mera dimaag thoda garam ho gaya hai, ek baar Refresh kar lijiye! ❤️"

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
