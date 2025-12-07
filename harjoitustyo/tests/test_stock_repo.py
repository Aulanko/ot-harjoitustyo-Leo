
import unittest
import pandas as pd
from unittest.mock import Mock, patch
from src.repositories.stock_repo import StockRepository, InvalidSymbol





class Test_Stock_Repository(unittest.TestCase):
    def setUp(self):
        self.repo = StockRepository()
        self.symbols = ["AAPL","GOOGL","MSFT"]



    def test_get_from_cache(self):
        self.repo.redis_client = None
        self.assertIsNone(self.repo._get_from_cache("opa"))
        self.repo.redis_client = Mock()
        self.repo.redis_client.get.return_value = "opa"

    
        self.repo.cache_enabled = True
        self.assertEqual("opa", self.repo._get_from_cache("opa"))
    
    def test_init_database(self):
        rep = StockRepository(db_path=":memory:")
        self.assertIsInstance(rep, StockRepository)

    
    def test_cache_key(self):
  
        k = self.repo.cache_key("AAPL", "current")
        
        self.assertIsInstance(k, str)
        self.assertEqual(k, "stock:AAPL:current")

    def test_set_to_cache(self):
        self.repo.cache_enabled = False
        self.assertIsNone(self.repo.set_to_cache("key", "data as str"))

    def test_get_current_data(self):

        with self.assertRaises(InvalidSymbol):
            self.assertIsNone(self.repo.get_current_data(symbol=None))

    def test_get_cached_current_data(self):
        self.repo._get_from_cache = Mock(return_value=None)
        vast = self.repo._get_cached_current_data("AAPL")
        self.assertIsNone(vast)

    def test_fetch_and_cache_current_data(self):
        with patch("yfinance.Ticker") as ticker:
            tikcer_instance = Mock()
            tikcer_instance.history.return_value = pd.DataFrame()
            ticker.return_value  = tikcer_instance
            vast = self.repo._fetch_and_cache_current_data("GOOGL")
        self.assertIsNone(vast)
    

    def test_get_historical_data(self):
        with patch("yfinance.Ticker") as ticker:
            ticker_instanc = Mock()
            ticker_instanc.history.return_value = pd.DataFrame([
                {'Date': pd.Timestamp('2025-12-04'),'High':146.5, 'Low': 141.2, 'Volume': 4200, 'Close': 144.1, 'Open': 142.7},
            {'Date': pd.Timestamp('2025-12-03'), 'High':149.3,'Low': 133.4, 'Volume': 6150, 'Close':147.2, 'Open': 146.1},
            {'Date': pd.Timestamp('2025-12-02'),'High': 144.7, 'Low': 138.9, 'Volume': 3950,'Close': 141.8, 'Open': 143.5},
            {'Date': pd.Timestamp('2025-12-01'), 'High': 151.6,'Low': 126.8,'Volume': 6280, 'Close':149.0, 'Open':147.3},
            {'Date': pd.Timestamp('2025-11-30'),'High': 146.2,'Low':139.7, 'Volume': 4100, 'Close': 143.0, 'Open': 142.1},
            {'Date': pd.Timestamp('2025-11-29'), 'High': 152.4,'Low': 123.6, 'Volume': 5900,'Close':147.9, 'Open':148.8},
            {'Date': pd.Timestamp('2025-11-28'),'High': 143.8,'Low': 139.4, 'Volume': 3800,'Close': 141.6, 'Open': 142.9},
            {'Date': pd.Timestamp('2025-11-27'), 'High': 149.9, 'Low': 122.7, 'Volume': 6050,'Close': 148.5, 'Open': 146.9},
            ])
            ticker.return_value = ticker_instanc

            vast = self.repo.get_historical_data("AAPL")
        self.assertIsInstance(vast, pd.DataFrame)
        self.assertIsNotNone(vast)



         
        

        

    
        




    


   



        

        

        










        

        








        

    
    
    

