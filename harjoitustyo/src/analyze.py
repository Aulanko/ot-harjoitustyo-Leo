
import statistics
import numpy as np

class Analyze():
    def __init__(self):
        pass

    def mean(self, stock_data_for_plotting):

        mean_value_from_high = statistics.mean(stock_data_for_plotting["High"])
        mean_value_from_low = statistics.mean(stock_data_for_plotting["Low"])
        true_mean = statistics.mean([mean_value_from_high, mean_value_from_low])

        return true_mean
    
    def maximum(self, stock_data_for_plotting):
        
        return max(stock_data_for_plotting["High"])
    
    def minimum(self, stock_data_for_plotting):
        return min(stock_data_for_plotting["Low"])
    
    def correlation(self, first_stoock_plot_data, second_stock_plot_data):
        correlation_matrix =np.corrcoef(first_stoock_plot_data["Close"], second_stock_plot_data["Close"])
        correlation = correlation_matrix[0,1]
        return correlation
    

    

    


