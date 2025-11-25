
import unittest

from src.models.stock import StockData
from datetime import datetime



class Test_StockData(unittest.TestCase):
    def setUp(self):
       
        self.stock_data = StockData(
            symbol="GOOG",
            timestamp = datetime.now(),
            high= 160.0,
            low=140.3,
            close=156.3,
            open=145.2,
            volume=38283
        )
    
    
  

    def test_correct_initialization(self):
        data=self.stock_data
        self.assertEqual("GOOG", data.symbol)
        self.assertEqual(160.0,data.high)
        self.assertEqual(140.3,data.low)

        self.assertEqual(156.3,data.close)
        self.assertEqual(145.2,data.open)
        self.assertEqual(38283,data.volume)
        

    def test_return_to_dict(self):

        data = self.stock_data.to_dict()
        self.assertIsInstance(data, dict)

    def test_validate_too_big_low(self):
        with self.assertRaises(ValueError):
            StockData(
                symbol="GOOG",
                timestamp = datetime.now(),
                high= 160.0,
                low=170.3,
                close=156.3,
                open=145.2,
                volume=38283
            )
    
    def test_negative_volume(self):
         with self.assertRaises(ValueError):
            StockData(
                symbol="GOOG",
                timestamp = datetime.now(),
                high= 160.0,
                low=70.3,
                close=156.3,
                open=145.2,
                volume=-38283
            )

    def test_price_change_percent(self):
        previous_close= 150
     
        answer = self.stock_data.price_change_percent(previous_close)
        expected = ((self.stock_data.close-previous_close)/previous_close)*100
        self.assertEqual(expected, answer)

    def test_price_change(self):
        previous_close = 150
        answer = self.stock_data.price_change(previous_close)
        excepted = self.stock_data.close-previous_close
        self.assertEqual(excepted, answer)


    
        

    