

import unittest
from unittest.mock import Mock, patch
from src.analysis.analyzer import StockAnalysis
from src.models.stock import  StockSummary, DataFactory, StockData
from src.repositories.stock_repo import StockRepository
from datetime import datetime, timedelta
import pandas as pd


class Test_StockAnalysis(unittest.TestCase):
    def setUp(self):
        self.mock = Mock(spec=StockRepository)
        self.analyzer = StockAnalysis(self.mock)
        self.symbols = ["AAPL", "GOOGL", "MSFT"]

      
        


    def test_get_current_data_for_multiple_symbols(self):
        mocks = {
            "GOOGL": StockData(symbol="GOOGL",high=150.0,low=145.0,volume=1000000, 
                               timestamp=datetime.now(),close=148.0, open_price=145
            ),
            "AAPL": StockData(symbol="AAPL", high=2800.0,low=2750.0,volume=500000,timestamp=datetime.now(),
                               close=2780.0,open_price=2800.0
            ),
            "MSFT": StockData(symbol="MSFT",high=340.0,low=335.0,volume=800000,timestamp=datetime.now(),
                              close=338.0,open_price=340.0
            )
        }
        self.mock.get_multiple_current_data.return_value = mocks




        vast = self.analyzer.get_current_data_for_multiple_symbols(symbols=self.symbols)

        self.assertIsInstance(vast,dict)
        self.assertEqual(vast["GOOGL"].close,148.0)
        self.assertEqual(vast["AAPL"].close,2780.0)
        self.assertEqual(vast["MSFT"].close,338.0)
        self.assertIn("AAPL",vast)
        self.assertIn("GOOGL",vast)
        self.assertIn("MSFT",vast)
        pass

    def test_get_histrical_data_analysis(self):
        mock_summary = StockSummary(
            symbol="AAPL",
            timestart=datetime.now() - timedelta(days=30),
            time_end=datetime.now(),
            high=150.0,
            low=120.0,
            volume_avg=20000.0,
            open_price=145,
            data_points=22
           
                )
        
        historical_data_mock = Mock()

        historical_data_mock.empty = False
        historical_data_mock.iterrows.return_value = [
        (pd.Timestamp('2024-01-01'),{'High': 145.0,'Low':140.0,'Volume':4000,'Close':142.0, 'Open':143}),
        (pd.Timestamp('2024-01-02'),{'High': 150.0,'Low':120.0,'Volume':6000,'Close':148.0, 'Open':145})
    ]
        self.mock.get_historical_data.return_value = historical_data_mock

        with patch('src.analysis.analyzer.DataFactory') as mock_factory:
            mock_factory.stock_data_summary.return_value = mock_summary
            vast = self.analyzer.get_histrical_data_analysis("AAPL")
            self.assertEqual(vast, mock_summary)
        
        self.mock.get_historical_data.assert_called_once_with("AAPL", "1mo")
        