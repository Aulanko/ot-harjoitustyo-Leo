

import logging
from typing import Dict, Optional, List

from models.stock import StockSummary, DataFactory, StockData
from repositories.stock_repo import StockRepository


class StockAnalysis:

    def __init__(self, repo: StockRepository):
        self.repo = repo
        self.logger = logging.getLogger(__name__)

    def get_current_data_for_multiple_symbols(
            self,
            symbols: List[str]
    ) -> Dict[str, Optional[StockData]]:
        try:
            res = self.repo.get_multiple_current_data(symbols)
            real_results = {symbol: data for symbol,
                            data in res.items() if data is not None}
            return real_results
        except (ValueError, ConnectionError) as e:
            self.logger.warning(
                "Unable to get current data from these symbols: %s. error: %s", symbols, e)
            return None

    def get_histrical_data_analysis(self, symbol: str, period: str = "1mo") -> StockSummary:
        try:
            historical_data = self.repo.get_historical_data(symbol, period)
            if historical_data.empty:
                raise ValueError(
                    "Got empty historical data from self.repo.get_historical_data")
            data_points = []

            for index, row in historical_data.iterrows():
                data_points.append(StockData(
                    symbol=symbol,
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    volume=int(row["Volume"]),
                    timestamp=index.to_pydatetime(),
                    close=float(row["Close"]),
                    open_price=float(row["Open"])
                ))
            answer = DataFactory.stock_data_summary(symbol, data_points)
            return answer
        except (ValueError, ConnectionError) as e:
            self.logger.warning(
                "historical_data_analysis failed on symbol: %s. %s", symbol, e)
            return None

    def calculate_over_bought_and_oversold(self, symbol: str):
        data_from_last_14_days = self.repo.get_historical_data(
            symbol=symbol, period="14d", interval="1d")
        current_data = self.repo.get_current_data(symbol=symbol)
        highest_high = max(data_from_last_14_days["High"])
        lowest_low = min(data_from_last_14_days["Low"])

        current_close = current_data.close

        williams_r = ((highest_high-current_close) /
                      (highest_high-lowest_low))*-100

        return williams_r

    def calculate_moving_averages(self, symbol: str):
        data_from_last_20_days = self.repo.get_historical_data(
            symbol=symbol, period="200d", interval="1d"
        )

        closed_list20 = data_from_last_20_days["Close"].tail(20).mean()
        closed_list50 = data_from_last_20_days["Close"].tail(50).mean()
        closed_list200 = data_from_last_20_days["Close"].mean()

        return {
            "closed_list20": closed_list20,
            "closed_list50": closed_list50,
            "closed_list200": closed_list200
        }
