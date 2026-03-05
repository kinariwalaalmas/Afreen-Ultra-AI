import streamlit as st
from groq import Groq
import google.generativeai as genai
from duckduckgo_search import DDGS
import yfinance as yf
from PIL import Image
import edge_tts
import asyncio
import base64

def get_clients():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"].strip())
    gemini = genai.GenerativeModel('gemini-1.5-flash')
    groq = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
    return gemini, groq

def speech_to_text(audio_bytes):
    """Mic Fix: Awaaz ko text mein badalna (Groq Whisper)"""
    try:
        _, groq_client = get_clients()
        # Audio file temporary save
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

def get_stock_price(ticker):
    """Live Stock Tracker (Surat Textile Stocks)"""
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")['Close'].iloc[-1]
        return f"{ticker}: ₹{price:.2f}"
    except: return ""

def get_news_ticker():
    """Live News for Top Ticker"""
    try:
        with DDGS() as ddgs:
            results = [r['title'] for r in ddgs.text("Surat textile market news 2026", max_results=3)]
            return " | ".join(results)
    except: return "Jaan, market news load ho rahi hai..."

def analyze_image(image_file):
    """Image Recognition (Fabric/Fashion Recognition)"""
    try:
        gemini_client, _ = get_clients()
        img = Image.open(image_file)
        response = gemini_client.generate_content(["Describe this fabric or clothing style in Hinglish for a business expert.", img])
        return response.text
    except: return "Jaan, image samajh nahi aayi."
