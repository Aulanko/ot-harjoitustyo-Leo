
import unittest
import sqlite3
import os
import tempfile
from src.repositories.stock_repo import StockRepository

class Test_Stock_Repository(unittest.TestCase):
    def setUp(self):
        self.repo = StockRepository()
        self.symbols = ["AAPL", "GOOGL", "MSFT"]

    
    def test_init_database(self):
        repo = StockRepository(db_path=":memory:")
        self.assertIsInstance(repo, StockRepository)
        

        








        

    
    
    

