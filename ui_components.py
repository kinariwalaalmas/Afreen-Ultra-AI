def render_plus_menu():
    with st.popover("＋"):
        st.write("### Tools")
        # Existing Mic & Photo options...
        
        st.divider()
        st.write("📈 Stock Analysis")
        ticker = st.text_input("Enter Ticker (e.g., RELIANCE.NS, NIFTYBEES.NS)", key="stock_ticker")
        return ticker # Ticker return karein
