import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta



class Finance_machine():
    def __init__(self):
        self.symbols = ["AAPL", "GOOGL", "MSFT"] 

        pass


    def get_last_n_data_points(self, symbols=None, interval="1m", n_points=15):
    
        data = {}
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1d", interval=interval)

                recent_data = hist.tail(n_points)
                
                data[symbol] = recent_data


                print(f"Last {len(recent_data)} data points for {symbol}:")
                print(recent_data[['High', 'Low','Close']])
                
            except Exception as errori:
                print(f"Error fetching {symbol}: {errori}")
        
        return data
    
    def __str__(self):
        stock_data = self.get_last_n_data_points(self.symbols, interval="1m", n_points=15)
        print(stock_data)






