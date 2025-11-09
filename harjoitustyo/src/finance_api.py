import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_last_n_data_points(symbols, interval="1m", n_points=15):
   
    data = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d", interval=interval)

            recent_data = hist.tail(n_points)
            
            data[symbol] = recent_data

            
            print(f"Last {len(recent_data)} data points for {symbol}:")
            print(recent_data[['Open','High', 'Low','Close', 'Volume']])
            
        except Exception as errori:
            print(f"Error fetching {symbol}: {errori}")
    
    return data


stock_data = get_last_n_data_points(["AAPL", "GOOGL", "MSFT"], interval="1m", n_points=15)
print(stock_data)