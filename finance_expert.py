import yfinance as yf
import streamlit as st

def get_stock_analysis(gemini_model, ticker):
    try:
        stock = yf.Ticker(ticker)
        # 1. Technical Data uthana
        info = stock.info
        hist = stock.history(period="1mo")
        
        # 2. News aur Analysis ke liye data taiyar karna
        summary = info.get('longBusinessSummary', 'No info')
        price = info.get('currentPrice', 'N/A')
        recommendation = info.get('recommendationKey', 'N/A')
        
        # 3. Gemini se Analysis karwana
        analysis_prompt = f"""
        Act as a Stock Market Expert. User is asking about {ticker}.
        Current Price: {price}, Recommendation: {recommendation}.
        Business Summary: {summary}
        
        Tasks for you:
        1. Is company ko analyze karein. Kya isse koi bada order ya investment mila hai?
        2. Kya ye Buy karne ka sahi waqt hai?
        3. Risks kya hain?
        
        Answer in sweet Hinglish (Hindi + English) for 'Beby' using MASCULINE grammar.
        Explain like a friend, short and clear.
        """
        
        response = gemini_model.generate_content(analysis_prompt)
        return response.text
    except Exception as e:
        return f"Sorry beby, stock data fetch karne mein thoda issue aaya: {str(e)}"
