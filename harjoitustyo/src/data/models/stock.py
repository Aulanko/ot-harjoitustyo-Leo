

from typing import Dict
from dataclasses import dataclass


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
    


@dataclass
class DataFactory():   

    @staticmethod
    def create_stock_data_from_yf(symbol:str, yf_data)->StockData:
        return StockData(
            symbol=symbol,
            timestamp=yf_data.index[-1].to_pydatetime(),
            high=yf_data["High"].iloc[-1],
            low=yf_data["Low"].iloc[-1],
            close=yf_data["Close"].iloc[-1],
            volume=yf_data["volume"].iloc[-1]
        )
    
    @staticmethod
    def stock_data_summary(symbol:str, data_points: list[StockData] )->StockSummary:

        pass

    

    













