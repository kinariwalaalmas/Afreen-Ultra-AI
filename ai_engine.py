import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import edge_tts
import asyncio
import base64

def get_clients():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception: return None, None

def get_ai_response(messages, search_info=""):
    """Auto-routing: Afreen khud dimaag chunegi"""
    gemini_client, groq_client = get_clients()
    system_prompt = f"You are Afreen, a professional Hinglish AI. Address user as 'Jaan' (Male). Context: {search_info}"
    
    user_query = messages[-1]["content"].lower()
    
    try:
        # Complex logic ya lambi baat ke liye DeepSeek use karegi
        if len(user_query) > 100 or "think" in user_query:
            model_id = "deepseek-r1-distill-llama-70b"
            res = groq_client.chat.completions.create(
                model=model_id,
                messages=[{"role": "system", "content": system_prompt}] + messages
            )
            return res.choices[0].message.content
        
        # Fast response ke liye Gemini 1.5 Flash
        else:
            chat = gemini_client.start_chat(history=[])
            response = chat.send_message(f"{system_prompt}\n\nUser: {user_query}")
            return response.text
    except:
        return "Jaan, mera ek dimaag thoda thak gaya hai, par main doosre se koshish kar rahi hoon..."

# --- Baki functions (Voice/Search) wese hi rahenge ---
async def generate_voice(text):
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+25%")
    await communicate.save("response.mp3")

def play_audio():
    try:
        with open("response.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

def web_search(query):
    try:
        with DDGS() as ddgs:
            res = [r for r in ddgs.text(query, max_results=2)]
            return res[0]['body'] if res else ""
    except: return ""

def transcribe_audio(client, audio_bytes):
    return client.audio.transcriptions.create(file=("audio.wav", audio_bytes), model="distil-whisper-large-v3-en").text
