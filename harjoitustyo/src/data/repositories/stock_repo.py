
import logging

import yfinance as yf
import pandas as pd
from redis import Redis

from abc import ABC, abstractmethod
from typing import Dict,List,Optional,Tuple, Optional
from dataclasses import dataclass

import sqlite3
import json
from datetime import datetime

from models.stock import StockSummary, DataFactory



class SpotStockDataError(Exception):
    def __init__(self, symbol:str, message: str = None):
        self.symbol = symbol
        self.message = message or f"An error occurred when doing operation on stockData symbol: {self.symbol}"
        super().__init__(self.message)

    def log_error(self):
        print(f"[SpotStockDataError] {self.symbol}:{self.message}")

    def dict_form_log(self):
        return {"stock_data for symbol": self.symbol, "message": self.message}

class DataSourceFailed(Exception):
    def __init__(self, source = None, message: str=None):
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


class BaseStockClass(ABC):


    @abstractmethod
    def get_current_data(self, symbol: str, )->Optional[StockData]:
    
        raise NotImplementedError("subclasses must implement get_current_data")


    @abstractmethod
    def get_historical_data(self, symbol : str, period:str ="1mo", interval : str="1d")->pd.DataFrame:
        raise NotImplementedError("subclasses must implement get_historical_data")
   
    @abstractmethod
    def get_multiple_current_data(self, symbols: List[str]) -> Dict[str, Optional[StockData]]:
        raise NotImplementedError("Subclasses must implement get_multiple_current_data")




class StockRepository(BaseStockClass):
    def __init__(self, db_path = "stocks.db", cache_enabled:bool=True):
        self.logger = logging.getLogger(__name__)
        self.cache_enabled = cache_enabled
       
        self.redis_client = None


        if cache_enabled:
            try:
                self.redis_client = Redis(host='localhost', port=6379, decode_responses=True)
                self.redis_client.ping()
            except Exception as e:
                self.logger.warning(f"Redis unavailable, lets use SQL lite instead. Error: {e} ")
                self.redis_client = None


       
        self.db_path = db_path
        self.init_database()


    def init_database(self):
        try:
            with sqlite3.connect(self.db_path) as connection:
                connection.execute("""CREATE TABLE IF NOT EXISTS Stock_hist 
                                   (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    symbol TEXT NOT NULL,
                                    high REAL NOT NULL,
                                    low  REAL NOT NULL,
                                    close REAL NOT NULL,
                                   
                                    volume INT NOT NULL,
                                   timestamp DATETIME NOT NULL 
                                   )
                                   """)
               
                connection.execute("CREATE INDEX IF NOT EXISTS idx_symbol_timestamp ON Stock_hist(symbol, timestamp)")
        except Exception as e:
            self.logger.warning(f"Error creating the db table:{e}")
            raise SpotStockDataError("Database initialization failed")
       
    def cache_key(self, symbol:str, data_type:str)->str:
        return f"stock:{symbol}:{data_type}"
       
    def get_from_cache(self, key:str)->Optional[str]:
        if not self.cache_enabled or self.redis_client==None:
            return None
        try:
            return self.redis_client.get(key)
        except Exception as e:
            self.logger.warning(f"Failed to read cache: {e}")
            return None
       
    def set_to_cache(self, key:str, data:str, expire_seconds = 300)->None:
        if not self.cache_enabled or self.redis_client==None:
            return None
        try:
            self.redis_client.setex(key, expire_seconds, data)
        except Exception as e:
            self.logger.warning(f"failed to set the data to cache: {e}")
       
   
    def get_current_data(self, symbol:str)->Optional[StockData]:


        if not symbol or isinstance(symbol,str)==False:
            raise InvalidSymbol(f"invalid symbol or not symbol at all")
       
        cache_key = self.cache_key(symbol, "current")
        cached_data = self.get_from_cache(cache_key)


        if cached_data:
            try:
                cache_dict = json.loads(cached_data)

                cache_dict["timestamp"] =datetime.fromisoformat(cache_dict["timestamp"])
                return StockData(**cache_dict)
            except Exception as e:
                raise SpotStockDataError(symbol, f"error getting stock data from cache: {e}")
               
        try:
            ticker = yf.Ticker(symbol)
            time_frame = ticker.history(period="1d", interval="1m")
            if time_frame.empty:
                self.logger.warning(f"No stock data available for symbol: {symbol}")
                return None
           
            #last = time_frame.iloc[-1]

            stock_data = DataFactory(symbol, time_frame)

        #    stock_data = StockData(  
         #       symbol=symbol,
          #      timestamp= time_frame.iloc[-1].to_pydatetime(),
           #     high= float(last["High"]),
            #    low= float(last["Low"]),
             #   close= float(last["Close"]),
              #  volume= int(last["Volume"])
            #)


            try:
                self.set_to_cache(cache_key, json.dumps({
                    "symbol": stock_data.symbol,
                    "low": stock_data.low,
                    "high": stock_data.high,
                    "close": stock_data.close,
                    "volume": stock_data.volume,
                    "timestamp":stock_data.timestamp.isoformat()
                }))
            except Exception as e:
                self.logger.warning(f"Failed to set cahce data for {symbol}: {e}")
           
        except Exception as e:
            self.logger.warning(f"The operation to get current data failed for {symbol}: {e}")
            raise DataSourceFailed(f"Error with the data source: {e}")
        
        return stock_data


    def get_historical_data(self, symbol:str, period:str = "1mo", interval:str = "1d")->pd.DataFrame:

        try:
            ticker = yf.Ticker(symbol)
            time_frame = ticker.history(period=period, interval=interval)
            if time_frame.empty:
                self.logger.warning(f"No historical stock data available for symbol: {symbol}")
                return pd.DataFrame()
            return time_frame
           
        except Exception as e:
            self.logger.warning(f"failed to fetch historical data for {symbol}: {e}")
            raise DataSourceFailed(f"Perhaps no data source for this symbol {symbol}: {e}")
        
    def get_multiple_current_data(self, symbols:List[str],) ->Dict[str, Optional[StockData]]:
        results = {}

        for symbol in symbols:
            try:
                results[symbol]=self.get_current_data(symbol)
            except (InvalidSymbol, DataSourceFailed) as e:
                self.logger.error(f"failed to fetch data: {e}")
                results[symbol] = None
        
        return results

    
    def store_historical_data(self, stock_data:StockData)->None:
        try:
            with sqlite3.connect(self.db_path) as connection:
                connection.execute("""INSERT INTO Stock_hist (symbol, timestamp, high, low,close,
                                   volume)
                                   VALUES (?,?,?,?,?,?)  """, (
                                       stock_data.symbol,
                                       stock_data.timestamp,
                                       stock_data.high,
                                       stock_data.low,
                                       stock_data.close,
                                       stock_data.volume
                                   ))
        except Exception as e:
            self.logger.warning(f"Failed to save stock data into the Stock_hist table: {e}")

        


