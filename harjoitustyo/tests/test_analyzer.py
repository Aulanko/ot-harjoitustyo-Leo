

import unittest
from unittest.mock import Mock, patch
from src.analysis.analyzer import StockAnalysis
from src.models.stock import  StockSummary, StockData
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

    def test_calculate_over_bought_and_over_sold(self):

        mock_stock_data =  StockData(symbol="GOOGL",high=150.0,low=145.0,volume=1000000, 
                               timestamp=datetime.now(),close=148.0, open_price=145)

        
        mock_data_from_last_14_days = pd.DataFrame([
            {'Date': pd.Timestamp('2025-12-04'),'High':146.5, 'Low': 141.2, 'Volume': 4200, 'Close': 144.1, 'Open': 142.7},
            {'Date': pd.Timestamp('2025-12-03'), 'High':149.3,'Low': 133.4, 'Volume': 6150, 'Close':147.2, 'Open': 146.1},
            {'Date': pd.Timestamp('2025-12-02'),'High': 144.7, 'Low': 138.9, 'Volume': 3950,'Close': 141.8, 'Open': 143.5},
            {'Date': pd.Timestamp('2025-12-01'), 'High': 151.6,'Low': 126.8,'Volume': 6280, 'Close':149.0, 'Open':147.3},
            {'Date': pd.Timestamp('2025-11-30'),'High': 146.2,'Low':139.7, 'Volume': 4100, 'Close': 143.0, 'Open': 142.1},
            {'Date': pd.Timestamp('2025-11-29'), 'High': 152.4,'Low': 123.6, 'Volume': 5900,'Close':147.9, 'Open':148.8},
            {'Date': pd.Timestamp('2025-11-28'),'High': 143.8,'Low': 139.4, 'Volume': 3800,'Close': 141.6, 'Open': 142.9},
            {'Date': pd.Timestamp('2025-11-27'), 'High': 149.9, 'Low': 122.7, 'Volume': 6050,'Close': 148.5, 'Open': 146.9},
        ])

        self.mock.get_historical_data.return_value = mock_data_from_last_14_days
        self.mock.get_current_data.return_value = mock_stock_data
        current_close = mock_stock_data.close

        highest_high = max(mock_data_from_last_14_days["High"])
        lowest_low = min(mock_data_from_last_14_days["Low"])

        test_williams_r = ((highest_high-current_close) /
                      (highest_high-lowest_low))*-100
        
        vast = self.analyzer.calculate_over_bought_and_oversold("GOOGL")
    
        self.assertEqual(test_williams_r,vast)

    def test_empty_on_historical(self):
        his_data = Mock()
        his_data.empty = True
        self.mock.get_historical_data.return_value = his_data
        vast = self.analyzer.get_histrical_data_analysis("AAPL")
        self.assertIsNone(vast)

    def test_get_multiple_symbols_failifng(self):

        self.mock.get_multiple_current_data.side_effect = ConnectionError("Error networking")

        vast = self.analyzer.get_current_data_for_multiple_symbols(symbols=self.symbols)
        self.assertIsNone(vast)

    def test_hist_dataa_erro(self):
        self.mock.get_historical_data.side_effect = ValueError("Opaa, invalidi symbol")
        vast = self.analyzer.get_histrical_data_analysis("Inva leadi")
        self.assertIsNone(vast)



        


   


        


        