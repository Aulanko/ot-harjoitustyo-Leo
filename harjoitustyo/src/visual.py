import matplotlib.pyplot as plt


class Visualize():
    def __init__(self):

        pass

    def make_a_graph_from_prices(self, stock_data, column_to_get_data, symbol):

        plt.figure(figsize=(30, 6))
        what_times = [str(row).split(' ')[1][3:5] for row in stock_data.index]

        values = stock_data[column_to_get_data].values

        plt.bar(what_times, values)

        min_price = min(values)
        max_price = max(values)

        price_ranger = max_price-min_price

        plt.ylim(min_price - price_ranger * 0.1,
                 max_price + price_ranger * 0.1)

        plt.title("Price graph from the first company of symbols list (Apple)")

        plt.xlabel("Time (-5 hours from englan greenwitch)")

        plt.ylabel("price")

        return plt.gcf()

    def display_visualization(self, data):
        for symbol, stock_data in data.items():
            if stock_data.empty:
                return
