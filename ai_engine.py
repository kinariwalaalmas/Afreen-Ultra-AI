import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import edge_tts
import asyncio
import base64
import os

def get_clients():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception: return None, None

def deep_scanner(query):
    """Simple web search for IDs and details"""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(f'"{query}" info', max_results=3)]
            return "\n".join([f"- {r['body']}" for r in results])
    except: return ""

def get_ai_response(messages, context=""):
    clients = get_clients()
    if not clients: return "Jaan, API Keys missing hain!"
    gemini_client, groq_client = clients
    system_prompt = f"You are Afreen. Speak in sweet Hinglish. Address user as 'Jaan'. Context: {context}"
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
    try:
        clean = text.replace('*', '').replace('#', '')
        communicate = edge_tts.Communicate(clean, "hi-IN-SwaraNeural", rate="+15%")
        await communicate.save("response.mp3")
    except: pass

def play_audio():
    try:
        if os.path.exists("response.mp3"):
            with open("response.mp3", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass
