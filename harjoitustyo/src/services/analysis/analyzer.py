

import logging
from data.models.stock import StockSummary, DataFactory, StockData
from  data.repositories.stock_repo import StockRepository, SpotStockDataError, InvalidSymbol

class StockAnalysis:

    def __ini__(self, repo:StockRepository):
        self.repo = repo
        self.logger = logging.getLogger(__name__)
