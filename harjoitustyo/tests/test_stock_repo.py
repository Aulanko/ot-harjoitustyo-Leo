
import unittest
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

        

    
        




    


   



        

        

        










        

        








        

    
    
    

