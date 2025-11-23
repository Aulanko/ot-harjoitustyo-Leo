

import logging
from typing import Dict, Optional, List
from data.models.stock import StockSummary, DataFactory, StockData
from  data.repositories.stock_repo import StockRepository, SpotStockDataError, InvalidSymbol
import pandas as pd

class StockAnalysis:

    def __ini__(self, repo:StockRepository):
        self.repo = repo
        self.logger = logging.getLogger(__name__)

    def get_current_data_for_multiple_symbols(self, symbols:List[str])->Dict[str,Optional[StockData]]:
        try:
            res = self.repo.get_multiple_current_data(symbols)
            real_results = {symbol:data for symbol,data in res.items() if data is not None}
            return real_results
        except Exception as e:
            self.logger.warning(f"Unable to get current data from these symbols: {symbols}")
            return None

        pass

    def get_histrical_data_analysis(self, symbol: str, period: str="1mo")->StockSummary:
        try:
            historical_data = self.repo.get_historical_data(symbol, period)
            if historical_data.empty:
                raise ValueError(f"Got empty historical data from self.repo.get_historical_data")
            dataPoints = []

            for index, row in historical_data.iterrows():
                dataPoints.append(StockData(
                    symbol=symbol,
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    volume=int(row["Volume"]),
                    timestamp=index.to_pydatetime(),
                    close=float(row["Close"])
                ))
            answer = DataFactory.stock_data_summary(symbol,dataPoints)
            return answer
        except Exception as e:
            self.logger.warning(f"historical_data_analysis failed on symbol: {symbol}. {e}")

    




