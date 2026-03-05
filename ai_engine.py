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
    """API clients setup"""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except: return None, None

def speech_to_text(audio_bytes):
    """Awaaz ko text mein badalna"""
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
    except: return None

def get_news_ticker():
    """Market news scan karna"""
    try:
        with DDGS() as ddgs:
            results = [r['title'] for r in ddgs.text("Surat textile news 2026", max_results=3)]
            return " | ".join(results)
    except: return "Jaan, market news load ho rahi hai..."

def analyze_image(image_file):
    """Kapde ki photo analyze karna"""
    try:
        gemini_client, _ = get_clients()
        img = Image.open(image_file)
        response = gemini_client.generate_content(["Is kapde ka style aur fabric Hinglish mein batao Jaan ke liye.", img])
        return response.text
    except: return "Jaan, photo samajh nahi aayi."

def get_ai_response(messages, context=""):
    """Afreen ka smart response"""
    clients = get_clients()
    if not clients: return "Jaan, API Keys missing hain!"
    gemini_client, groq_client = clients
    system_prompt = f"You are Afreen Ultra. Speak in sweet Hinglish. Always address user as 'Jaan'. Context: {context}"
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
    """Natural voice generation"""
    try:
        clean = text.replace('*', '').replace('#', '')
        communicate = edge_tts.Communicate(clean, "hi-IN-SwaraNeural", rate="+20%")
        await communicate.save("response.mp3")
    except: pass

def play_audio():
    """Audio playback fix"""
    try:
        if os.path.exists("response.mp3"):
            with open("response.mp3", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

def deep_scanner(query):
    """Web search logic"""
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(query, max_results=3)]
            return "\n".join(results)
    except: return ""
