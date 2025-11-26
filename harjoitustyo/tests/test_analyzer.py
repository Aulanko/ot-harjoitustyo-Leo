

import unittest

from src.analysis.analyzer import StockAnalysis

class Test_StockAnalysis(unittest.TestCase):
    def setUp(self):
        self.analyzer = StockAnalysis()
        self.symbols = ["AAPL", "GOOGL", "MSFT"] 

    