
import logging

from typing import Dict,List,Optional,Tuple, Optional
from dataclasses import dataclass

import sqlite3
import json
from datetime import datetime





@dataclass
class StockData(): 
    symbol : str
    timestamp : datetime
    high: float
    low: float
    close: float
    volume: int=0

   
    def to_dict(self)->Dict:
        return{
            "symbol" : self.symbol,
            "timestamp" : self.timestamp,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume
        }
    
    @classmethod
    def create_stock_data_from_dict(cls, data:Dict)->Dict:
        data = data.copy()
        if isinstance(data["timestamp"],str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        
        return cls(**data)
    

    def price_change(self, previous_close: float)->float:
        return self.close - previous_close
    
    def price_change_percent(self, previous_close:float)->float:
        ans = self.close-previous_close
        return (ans/self.close)*100
    

@dataclass
class StockSummary():

    symbol : str
    timestart : datetime
    time_end: datetime
    high: float
    low: float
    volume_avg: float
    data_points: int=0


    @property
    def price_change_range(self):
        return self.high-self.low
    
    @property
    def volatility(self):
        average = (self.high+self.low)/2
        return (self.price_change_range/average)*100
    
    
    










