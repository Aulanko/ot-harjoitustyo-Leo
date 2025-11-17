

import unittest
from src.finance_api import Finance_machine


class Test_Finance_machine(unittest.TestCase):
    def setUp(self):
        self.finance_machine = Finance_machine()
      
        self.symbols = ["AAPL", "GOOGL", "MSFT"] 
        


        pass

    def test_get_last_n_data_points(self):
        data = self.finance_machine.get_last_n_data_points(self.symbols, "1m", 3)

        self.assertIsInstance(data, dict)
        self.assertEqual(len(self.symbols), len(data))

    


