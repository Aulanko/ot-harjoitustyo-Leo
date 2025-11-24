
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QGridLayout, QTextEdit,
                             QPushButton, QLineEdit)
from PyQt6.QtCore import QSize, Qt
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from typing import Dict, Optional
import logging

from analysis.analyzer import StockAnalysis
from models.stock import StockData, StockSummary
from repositories.stock_repo import StockRepository


class DataTickerWidget(QLabel):

    def __init__(self, symbol:str, price: float, change:float):
        super().__init__()
        self.symbol = symbol
        self.stock_service = None
        self.price = price
        self.change = change
        self.color = ""
        self.sign = ""
        self.setUpUI()

    def setUpUI(self):
        


        layout = QVBoxLayout()
        self.setLayout(layout)
     
        self.symbol_label = QLabel(f"{self.symbol}")
        self.price_label = QLabel(f"{self.price}$")
        self.change_label = QLabel()
        

        layout.addWidget(self.symbol_label)
        layout.addWidget(self.price_label)
        layout.addWidget(self.change_label)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
    def update_data(self, price:float, change:float):
        self.price = price
        self.change = change

        if self.change >=0:
            self.color ="green"
            self.sign="+"
        else:
            self.color="red"
            self.sign ="-"

        self.price_label.setText(f"{price}$")
        self.change_label.setText(f"{self.sign}{abs(self.change)}%")
        self.change_label.setStyleSheet(f"color: {self.color}")
        self.setUpUI()




    pass




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.CurrentSymbols = ["AAPL","GOOGL"]
        self.setUpUI()
        self.logger = logging.getLogger(__name__)
        self.repo = StockRepository()
        self.analyzer = StockAnalysis(self.repo)
        

        

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
        analyze_button.clicked.connect(self.refresh_data)

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
            current_data = self.analyzer.get_current_data_for_multiple_symbols(self.CurrentSymbols)
            if current_data:
                self.update_data_ticker_widgets(current_data)
                self.update_displayed_data(current_data)
        except Exception as e:
            self.logger.warning(f"error on refresh_data: {e}")
    
    def update_data_ticker_widgets(self, stock_data: Dict[str,StockData]):
       
       for symbol, data in stock_data.items():
           if data and symbol in self.data_ticker_widgets:
               
               change_percentage = (data.close-data.open)/data.open*100
               self.data_ticker_widgets[symbol].update_data(data.close, change_percentage)



    def update_displayed_data(self, stock_data:Dict[str, StockData]):
        texti = "Stock data \n\n"

        for symbol, data in stock_data.items():
            if data:
                real_change_percent = (data.close-data.open)/data.open*100
                
                
                texti += f"symbol: {symbol}\n"
                texti += f"Timestamp on close: {data.timestamp.replace(tzinfo=None)}\n"
                texti +=f"change: {real_change_percent} \n"
                texti +=f"opening price: {data.open} \n"
                texti +=f"closing price: {data.close} \n"
                texti +=f"Volume: {data.volume} \n"

        self.data_Display.setText(texti)
                










def main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__=="__main__":
    main_window()