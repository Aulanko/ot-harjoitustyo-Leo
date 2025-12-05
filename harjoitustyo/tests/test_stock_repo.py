
import unittest
from unittest.mock import MagicMock
from src.repositories.stock_repo import StockRepository

class Test_Stock_Repository(unittest.TestCase):
    def setUp(self):
        self.repo = StockRepository()
        self.symbols = ["AAPL", "GOOGL", "MSFT"]

    
    def test_init_database(self):
        repo = StockRepository(db_path=":memory:")
        self.assertIsInstance(repo, StockRepository)

    def test_cache_key(self):
        vast = self.repo.cache_key("AAPL", "current")
        self.assertIsInstance(vast, str)
        self.assertEqual("stock:AAPL:current", vast)

    def test_get_from_cache(self):
        self.repo.cache_enabled = False
        self.assertIsNone(self.repo._get_from_cache("testaa_key"))
        self.repo.redis_client = None
        self.assertIsNone(self.repo._get_from_cache("testaa_key"))

        self.repo.cache_enabled = True
        self.repo.redis_client = MagicMock()
        self.repo.redis_client.get.return_value = "testaa_key"
        vast = self.repo._get_from_cache("testaa_key")

        self.assertEqual(vast, "testaa_key")








        

        








        

    
    
    

