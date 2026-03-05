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

def speech_to_text(audio_bytes):
    """Whisper Turbo: Aapki awaaz ko turant samajhna"""
    try:
        _, groq_client = get_clients()
        with open("temp_audio.wav", "wb") as f: f.write(audio_bytes)
        with open("temp_audio.wav", "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=("temp_audio.wav", file.read()),
                model="whisper-large-v3-turbo",
                language="hi"
            )
        return transcription.text
    except: return None

def get_ai_response(messages, context=""):
    clients = get_clients()
    gemini_client, groq_client = clients
    
    # ✨ Super Assistant Personality + Device Control
    system_prompt = f"""You are Afreen Ultra. Your Creator/Owner is **Almas Shaikh**. 
    1. Address Almas as 'Jaan' (Male grammar). 
    2. You can control the device: Open Apps, Camera, Flashlight, Screenshot, etc.
    3. If Jaan says 'Hey Afreen', be extra sweet and ready for action.
    4. Speak ONLY in natural Hinglish.
    Context: {context}"""
    
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
        clean = text.replace('*', '').replace('#', '')
        communicate = edge_tts.Communicate(clean, "hi-IN-SwaraNeural", rate="+20%", pitch="+5Hz")
        await communicate.save("response.mp3")
    except: pass

def play_audio():
    try:
        if os.path.exists("response.mp3"):
            with open("response.mp3", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass
