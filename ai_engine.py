import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import edge_tts
import asyncio
import base64

# --- Clients Setup ---
def get_clients():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception as e:
        return None, None

# --- AI Response Logic ---
def get_ai_response(brain, messages, search_info=""):
    system_prompt = f"You are Afreen, a sweet Hinglish girl. Address user as 'Jaan' and use MASCULINE grammar. Context: {search_info}"
    _, groq_client = get_clients()
    
    model_id = "llama-3.3-70b-versatile" if brain == "Llama 3.3 (Fast)" else "deepseek-r1-distill-llama-70b"
    
    res = groq_client.chat.completions.create(
        model=model_id,
        messages=[{"role": "system", "content": system_prompt}] + messages
    )
    return res.choices[0].message.content

# --- Search & Voice ---
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
    try:
        with open("response.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

def transcribe_audio(client, audio_bytes):
    return client.audio.transcriptions.create(file=("audio.wav", audio_bytes), model="distil-whisper-large-v3-en").text
