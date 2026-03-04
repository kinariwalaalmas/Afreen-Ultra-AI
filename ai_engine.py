import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS # Free unlimited search ke liye
import edge_tts
import asyncio
import base64

# --- 1. Clients Setup ---
def get_clients():
    # Groq client initialize karna
    try:
        groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return groq_client
    except Exception as e:
        st.error(f"Jaan, Groq API key mein issue hai: {e}")
        return None

# --- 2. Free Web Search (DuckDuckGo) ---
def web_search(query):
    """Bina kisi API key ke internet se news dhoondne ke liye"""
    try:
        with DDGS() as ddgs:
            # Top 3 results nikalna
            results = [r for r in ddgs.text(query, max_results=3)]
            if results:
                # Pehle result ki main body return karna
                return results[0]['body']
        return "Jaan, internet par is baare mein kuch naya nahi mila."
    except Exception as e:
        return f"Search fail ho gaya: {str(e)}"

# --- 3. Natural Voice Engine (Edge-TTS) ---
async def generate_voice(text):
    """Realistic awaaz generate karna"""
    # Rate +25% rakha hai taaki robotic na lage
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural", rate="+25%")
    await communicate.save("response.mp3")

def play_audio():
    """Audio file ko background mein play karna"""
    try:
        with open("response.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Audio play nahi ho paya, Jaan: {e}")

# --- 4. Voice to Text (Whisper) ---
def transcribe_audio(groq_client, audio_bytes):
    """Mic ki awaaz ko text mein badalna"""
    try:
        transcription = groq_client.audio.transcriptions.create(
            file=("audio.wav", audio_bytes),
            model="distil-whisper-large-v3-en"
        )
        return transcription.text
    except Exception as e:
        return f"Aapki awaaz samajh nahi aayi, Jaan: {e}"
