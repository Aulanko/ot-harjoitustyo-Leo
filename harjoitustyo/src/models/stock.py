

from typing import Dict
from dataclasses import dataclass


from datetime import datetime


@dataclass
class StockData:
    symbol: str
    timestamp: datetime
    high: float
    low: float
    close: float
    open: float
    volume: int = 0

    def to_dict(self) -> Dict:
        return {
            "symbol": self.symbol,
            "timestamp": self.timestamp.isoformat(),
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "open": self.open,
            "volume": self.volume
        }

    def __post_init__(self):
        self.validate()

    def validate(self):
        if self.high < self.low:
            raise ValueError(f"How can the lowest value be more than the highest value \
                             Highest: {self.high}, Lowest: {self.low}")

        if self.volume < 0:
            raise ValueError(
                f"Volume canot be negative. Volume: {self.volume}")

    @classmethod
    def create_stock_data_from_dict(cls, data: Dict) -> "StockData":
        data = data.copy()
        if isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])

        return cls(**data)

    def price_change(self, previous_close: float) -> float:
        return self.close - previous_close

    def price_change_percent(self, previous_close: float) -> float:
        if previous_close == 0:
            return 0.0
        ans = self.close-previous_close

        return (ans/previous_close)*100
    
    


@dataclass
class StockSummary:

    symbol: str
    timestart: datetime
    time_end: datetime
    high: float
    low: float
    volume_avg: float
    open:float
    data_points: int = 0
    

    @property
    def price_change_range(self):
        return self.high-self.low

    @property
    def volatility(self):
        average = (self.high+self.low)/2
        if average == 0:
            return 0
        return (self.price_change_range/average)*100


@dataclass
class DataFactory():

    @staticmethod
    def create_stock_data_from_yf(symbol: str, yf_data) -> StockData:
        return StockData(
            symbol=symbol,
            timestamp=yf_data.index[-1].to_pydatetime(),
            high=yf_data["High"].iloc[-1],
            low=yf_data["Low"].iloc[-1],
            close=yf_data["Close"].iloc[-1],
            open=float(yf_data["Open"].iloc[-1]),
            volume=yf_data["Volume"].iloc[-1]
        )

    @staticmethod
    def stock_data_summary(symbol: str, data_points: list[StockData]) -> StockSummary:

        if not data_points:
            raise ValueError(f"No data points were provided to the stock_data_summary static method, \
            symbol: {symbol}")
        high = [dp.high for dp in data_points]
        low = [dp.low for dp in data_points]
        volume = [dp.volume for dp in data_points]
        
        

        return StockSummary(
            symbol=symbol,
            timestart=min(dp.timestamp for dp in data_points),
            time_end=max(dp.timestamp for dp in data_points),
            high=max(high),
            low=min(low),
            volume_avg=(sum(volume))/len(volume),
            data_points=len(data_points)
            
            
        )
