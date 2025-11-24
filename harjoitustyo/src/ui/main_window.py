
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QGridLayout, QTextEdit,
                             QPushButton, QLineEdit)
from PyQt6.QtCore import QSize, Qt
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from typing import Dict, Optional

from services.analysis.analyzer import StockAnalysis
from data.models.stock import StockData, StockSummary


class DataTickerWidget(QLabel):

    def __init__(self, symbol:str, price: float, change:float):
        super().__init__()
        self.symbol = symbol
        self.price = price
        self.change = change
        self.color = ""
        self.sign = ""
        self.setUpUI()

    def setUpUI(self):
        if self.change >=0:
            self.color ="green"
            self.sign="+"
        else:
            self.color="red"
            self.sign ="-"


        layout = QVBoxLayout()
        self.setLayout(layout)
     
        self.symbol_label = QLabel(f"{self.symbol}")
        self.price_label = QLabel(f"${self.price}")
        self.change_label = QLabel(f"{self.sign}{abs(self.change)}%")
        self.change_label.setStyleSheet(f"color: {self.color}")

        layout.addWidget(self.symbol_label)
        layout.addWidget(self.price_label)
        layout.addWidget(self.change_label)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)





    pass




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.CurrentSymbols = ["AAPL","GOOGL"]
        self.setUpUI()
        

        

    def setUpUI(self):
        self.setWindowTitle("Stock data application")

        center_widget = QWidget()
        self.setCentralWidget(center_widget)
        main_layout = QHBoxLayout()
        center_widget.setLayout(main_layout)

        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)

        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel)



    

    def create_left_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        title = QLabel("Analyze Stocks")
        layout.addWidget(title)

        layout.addWidget(QLabel("Symbols:"))
        self.symbols = QTextEdit()

        layout.addWidget(self.symbols)

        symbol_layout = QHBoxLayout()
        self.new_symbol = QLineEdit()
        self.new_symbol.setPlaceholderText("Add a new symbol (for example; NVDA)")
        symbol_layout.addWidget(self.new_symbol)

        add_button = QPushButton("Add")
        #add_button.clicked.connect()
        symbol_layout.addWidget(add_button)
        layout.addLayout(symbol_layout)

        analyze_button = QPushButton("Analyze")
        #analyze_button.clicked.connect()

        layout.addWidget(analyze_button)

        return panel
    
    def create_right_panel(self):
        panel = QWidget()
        layout = QGridLayout()
        panel.setLayout(layout)

        self.data_ticker_widgets = {}
        for i, symbol in enumerate(self.CurrentSymbols):
            tick = DataTickerWidget(symbol, 0,0)
            self.data_ticker_widgets[symbol]= tick
            layout.addWidget(tick,0,i)

        self.PriceChart = FigureCanvas(Figure(figsize=(10,4)))
        layout.addWidget(self.PriceChart,1,0,1,len(self.CurrentSymbols))

        self.data_Display = QTextEdit()
        self.data_Display.setPlaceholderText("Stock Data shall appear..")
        layout.addWidget(self.data_Display,2,0,1,2)

        self.analysis_Display = QTextEdit()
        self.analysis_Display.setPlaceholderText("Analysis Data shall appear..")
        layout.addWidget(self.analysis_Display,2,2,1,2)



        return panel








   
    

    def refresh_data(self):
        try:
            current_data = StockAnalysis.get_current_data_for_multiple_symbols(self.CurrentSymbols)
            self.update_data_ticker_widgets()
        except Exception as e:
            self.logger.warning(f"error on refresh_data: {e}")
    
    def update_data_ticker_widgets(self, stock_data: Dict[str,StockData]):
       
       for symbol, data in stock_data.items():
           if data and symbol in self.data_ticker_widgets:
               if hasattr(data,"open"):
                change_percent = (data.close-data.open)/data.open*100

       return










def main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__=="__main__":
    main_window()