
import unittest
from src.analyze import Analyze
import pandas as pd



class Test_Analyze(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyze()
        self.symbols = ["AAPL", "GOOGL", "MSFT"] 
        self.highdata =[ 273.045502, 273.015015, 272.940002, 272.820007, 272.660004,
                         272.750000, 272.730011, 272.570007, 272.709991, 272.700012,
                         272.529602, 272.480011, 272.470001, 272.329987, 272.549988]
        
        self.low_data = [ 272.779999, 272.834991, 272.660004, 272.640015, 272.519989,
                          272.560089, 272.459991, 272.329987, 272.239990, 272.260010,
                          272.315002, 272.299988, 272.299988, 272.170013, 272.170013]
        
        self.close_data = [273.021698, 272.929993, 272.679993, 272.649994, 272.614990,
                           272.690002, 272.489990, 272.334991, 272.679993, 272.440002,
                           272.320007, 272.440002, 272.325012, 272.179993, 272.410004]
        
        self.dataframe = pd.DataFrame({"High": self.highdata, "Low":self.low_data, "Close":self.close_data })

        pass

    def test_maximum(self):
        maximi = self.analyzer.maximum(self.dataframe)
        biggest = max(self.highdata)
        self.assertEqual(maximi, biggest)

        pass

    def test_minimum(self):
        minimi = self.analyzer.minimum(self.dataframe)
        smallest = min(self.low_data)
        self.assertEqual(minimi, smallest)
        pass

    def test_mean(self):
        mean = self.analyzer.mean(self.dataframe)

        mean_high = sum(self.highdata)/len(self.highdata)
        mean_low = sum(self.low_data)/len(self.low_data)
        test_mean = (mean_high+mean_low)/2
       
        self.assertEqual(mean, test_mean)
        pass
