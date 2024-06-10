import streamlit as st
import yfinance as yf
import pandas as pd
st.set_page_config(page_title="Stock Analysis")
def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    df = stock.history(period="1mo")  # Adjust period as needed
    return df[['Open', 'High', 'Low', 'Close', 'Volume']]

def identify_downturns(index_df, threshold=1):
    index_df['Change'] = index_df['Close'].diff()
    index_df['Downturn'] = index_df['Change'] < 0
    index_df['DownturnPeriod'] = index_df['Downturn'].rolling(window=threshold).sum() == threshold
    return index_df[index_df['DownturnPeriod']]

def filter_strong_stocks(stock_df, downturn_periods):
    stock_df['Close'] = pd.to_numeric(stock_df['Close'], errors='coerce')
    stock_df['Change'] = stock_df['Close'].diff()
    downturn_dates = downturn_periods.index[downturn_periods['DownturnPeriod']]
    stock_df['RelativeStrength'] = stock_df.index.isin(downturn_dates) & (stock_df['Change'] > 0)
    strong_stocks = stock_df[stock_df['RelativeStrength']]
    return strong_stocks

# Streamlit user interface
st.title('Stock Analysis App')
symbols = st.text_input("Enter stock symbol(s), separated by commas (e.g., AAPL, MSFT, GOOGL)").upper().split(',')

if st.button('Analyze Stocks'):
    for symbol in symbols:
        symbol = symbol.strip()  # Trim any extra whitespace
        if symbol:
            with st.spinner(f'Fetching and analyzing {symbol}...'):
                # Fetch SP500 data for downturn analysis
                sp500_df = fetch_stock_data('SPY')
                downturn_periods = identify_downturns(sp500_df)

                # Fetch and analyze entered symbol
                stock_df = fetch_stock_data(symbol)
                strong_stocks = filter_strong_stocks(stock_df, downturn_periods)

                st.write(f"{symbol} :strength of stock(s) during downturn periods")
                st.dataframe(strong_stocks)

st.write("The Stock Analysis App is a Streamlit-based web application designed to help investors and financial analysts quickly and efficiently assess the strength of stocks during downturn periods of the S&P 500 index. Users can enter one or multiple stock symbols, and the app fetches historical stock data to identify which stocks performed strongly on days when the market was generally declining.")
