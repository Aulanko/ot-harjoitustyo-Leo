
import logging

import yfinance as yf
import pandas as pd
from redis import Redis

from abc import ABC, abstractmethod
from typing import Dict,List,Optional,Tuple, Optional
from dataclasses import dataclass

import sqlite3
import json
from datetime import datetime, timedelta

class SpotStockDataError(Exception):
    def __init__(self, stock_data, message: str = None):
        self.stock_data = stock_data
        self.message = message or f"An error occured when doing operation on stockData: {self.stock_data}"
        super().__init__(self.message)

    def log_error(self):
        print(f"[SpotStockDataError] {self.stock_data}:{self.message}")

    def dict_form_log(self):
        return {"stock_data": self.stock_data, "message": self.message}

class DataSourceFailed(Exception):
    def __init__(self, source, message: str=None):
        self.source = source
        self.message = message or f"An error occured when trying to fetch data from: {self.source}"
        super().__init__(self.message)

    def log_error(self):
        print(f"[DataSourceFailed] {self.source}:{self.message}")
    
    def dict_form_log(self):
        return {"source": self.source, "message": self.message}

class InvalidSymbol(Exception):
    def __init__(self, symbol, message: str = None):
        self.symbol = symbol
        self.message= message
        super().__init__(self.message)

    def log_error(self):
        print(f"[InvalidSymbol] {self.symbol}:{self.message}")
    
    def dict_form_log(self):
        return {"symbol": self.symbol, "message": self.message}
    



@dataclass
class StockData(): 
    symbol : str
    timestamp : datetime
    high: float
    low: float
    close: float
    volume: int=0



        

                



            






