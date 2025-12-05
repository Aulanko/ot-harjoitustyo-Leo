
import unittest
from unittest.mock import Mock, patch
from src.repositories.stock_repo import StockRepository





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


   



        

        

        










        

        








        

    
    
    

