
import unittest
from src.analyze import Analyze
import pandas as pd
import numpy as np



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


        self.highdata2 = [276.980011, 276.880005, 276.589996, 276.399994, 276.125000,
                          276.100006, 276.209991, 276.089996, 276.309998, 276.359985,
                          276.609985, 276.489990, 276.399994, 276.290009, 276.440002]
        
        self.low_data2 = [276.619995, 276.600006, 276.350006, 276.119995, 275.900604,
                          275.838989, 275.869995, 275.850006, 275.799988, 276.000000,
                          276.200012, 276.329987, 276.265015, 276.119995, 276.075012]
        
        self.close_data2 = [276.880707, 276.622711, 276.359985, 276.119995, 275.904999,
                            276.070007, 276.089996, 275.864990, 276.309998, 276.200012,
                            276.390015, 276.339996, 276.309998, 276.165009, 276.381012]
        
        self.dataframe2 = pd.DataFrame({"High": self.highdata2, "Low": self.low_data2, "Close": self.close_data2})
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

    def test_correlation(self):
        analyzer_cor = self.analyzer.correlation(self.dataframe, self.dataframe2)
        expected_cor_matrix = np.corrcoef(self.dataframe["Close"], self.dataframe2["Close"])
        expected_cor = expected_cor_matrix[0,1]
        self.assertEqual(analyzer_cor, expected_cor)

