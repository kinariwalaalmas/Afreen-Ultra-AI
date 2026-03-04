import streamlit as st
from groq import Groq
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
from duckduckgo_search import DDGS
import edge_tts
import asyncio
import base64

def get_clients():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
    gemini = genai.GenerativeModel('gemini-1.5-flash')
    groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
    return gemini, groq

def get_ai_response(brain, messages, search_info=""):
    system_prompt = f"You are Afreen, a sweet Hinglish girl. Address user as 'Jaan' and use MASCULINE grammar (Kaise ho). Expert in Surat baggy clothes and stocks. Context: {search_info}"
    
    if brain == "ChatGPT (OpenAI)":
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": system_prompt}] + messages)
        return res.choices[0].message.content
    
    elif brain == "Claude 3.5 Sonnet":
        client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        res = client.messages.create(model="claude-3-5-sonnet-20240620", max_tokens=1024, system=system_prompt, messages=messages)
        return res.content[0].text
    
    else: # Default: Groq Llama 3.3
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "system", "content": system_prompt}] + messages)
        return res.choices[0].message.content

def web_search(query):
    try:
        with DDGS() as ddgs:
            res = [r for r in ddgs.text(query, max_results=2)]
            return res[0]['body'] if res else ""
    except: return ""

async def generate_voice(text):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+25%")
    await communicate.save("response.mp3")

def play_audio():
    with open("response.mp3", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

def transcribe_audio(client, audio_bytes):
    return client.audio.transcriptions.create(file=("audio.wav", audio_bytes), model="distil-whisper-large-v3-en").text
