
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

    @classmethod
    def to_dict(self)->Dict:
        return{
            "symbol" : self.symbol,
            "timestamp" : self.timestamp,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume
        }
    



