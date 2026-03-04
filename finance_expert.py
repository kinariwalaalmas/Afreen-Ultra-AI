import yfinance as yf

def get_stock_analysis(gemini_model, ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice', 'N/A')
        
        prompt = f"""
        Analyze {ticker} with current price {price}. 
        Explain if 'Beby' should buy it for his long-term investment.
        Mention any big news or orders.
        Answer in sweet Hinglish using MASCULINE grammar (e.g. 'Aap le sakte ho').
        """
        return gemini_model.generate_content(prompt).text
    except Exception as e:
        return f"Sorry beby, data nahi mila: {e}"
