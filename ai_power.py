import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
from PIL import Image
import os

def get_ai_clients():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
        gemini = genai.GenerativeModel('gemini-1.5-flash')
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
        return gemini, groq
    except Exception: return None, None

def pinterest_fashion_search(query):
    """Pinterest search for Sir's business"""
    try:
        with DDGS() as ddgs:
            res = [r['image'] for r in ddgs.images(f"{query} fashion clothes pinterest", max_results=3)]
            return res
    except: return []

def deep_scanner(query):
    """Web search for general info or URLs"""
    try:
        with DDGS() as ddgs:
            search_q = f"details about {query}" if "http" in query.lower() else query
            results = [r['body'] for r in ddgs.text(search_q, max_results=3)]
            return "\n".join(results)
    except: return ""

def ai_brain(messages, context=""):
    """Afreen's Intelligence for Sir"""
    try:
        _, groq_client = get_ai_clients()
        system_prompt = f"Tum Afreen ho, Almas Sir ki Personal Assistant. Sweet Hinglish bolo. Context: {context}"
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages[-5:]
        )
        return response.choices[0].message.content
    except: return "Sir, main thoda thak gayi hoon, phir se puchiye na? ❤️"

def visual_scanner(image_file):
    try:
        gemini_client, _ = get_ai_clients()
        img = Image.open(image_file)
        res = gemini_client.generate_content(["Analyze this for Almas Sir's business.", img])
        return res.text
    except: return "Sir, scan nahi ho paya."

def get_news_ticker():
    try:
        with DDGS() as ddgs:
            res = [r['title'] for r in ddgs.text("Surat clothing market 2026", max_results=3)]
            return " 🔥 " + " | ".join(res)
    except: return "Sir, updates load ho rahi hain..."

def speech_to_text(audio_bytes):
    try:
        _, groq_client = get_ai_clients()
        with open("temp.wav", "wb") as f: f.write(audio_bytes)
        with open("temp.wav", "rb") as f:
            return groq_client.audio.transcriptions.create(file=("temp.wav", f.read()), model="whisper-large-v3-turbo", language="hi").text
    except: return None
