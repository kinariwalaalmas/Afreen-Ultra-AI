import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
from PIL import Image

def get_ai_clients():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
    gemini = genai.GenerativeModel('gemini-1.5-flash')
    groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
    return gemini, groq

def ai_brain(messages, context=""):
    """Afreen's Smart Thinking"""
    _, groq_client = get_ai_clients()
    system_prompt = f"You are Afreen Ultra. Owner: Almas Shaikh. Speak sweet Hinglish. Context: {context}"
    res = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}] + messages
    )
    return res.choices[0].message.content

def visual_scanner(image_file):
    """Fashion Recognition Power"""
    gemini_client, _ = get_ai_clients()
    img = Image.open(image_file)
    response = gemini_client.generate_content(["Analyze this for Almas Shaikh's business.", img])
    return response.text
