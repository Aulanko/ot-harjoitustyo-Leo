

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QPushButton, QLabel,
                            QTextEdit, QSplitter)
from PyQt6.QtCore import Qt

from finance_api import Finance_machine


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Financial Data App")
        self.setGeometry(100,100,800,600)
        self.finance_machine = Finance_machine()
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        
        
        stock_layout = QHBoxLayout()
        stock_layout.addWidget(QLabel("Stock symbol:"))
        
        self.stock_input = QLineEdit()
        self.stock_input.setPlaceholderText("AAPL, GOOGL, MSFT")
        self.stock_input.setFixedWidth(120)
        stock_layout.addWidget(self.stock_input)

        self.load_btn = QPushButton("Load Data")
        self.load_btn.setFixedWidth(100)
        self.load_btn.clicked.connect(self.load_data)  
        stock_layout.addWidget(self.load_btn)

        main_layout.addLayout(stock_layout)

       
        content_splitter = QSplitter(Qt.Orientation.Horizontal)

        
        self.data_display = QTextEdit()
        self.data_display.setPlaceholderText("Stock data will appear here")

        
        self.analysis_panel = QTextEdit()
        self.analysis_panel.setPlaceholderText("Analysis will appear here")

        self.data_visualization = QTextEdit()
        self.data_visualization.setPlaceholderText("Data visualization will appear here")

        content_splitter.addWidget(self.data_display)
        content_splitter.addWidget(self.analysis_panel)
        content_splitter.addWidget(self.data_visualization)
        

        content_splitter.setSizes([400,400,400])

        main_layout.addWidget(content_splitter)

        self.status_label = QLabel("Ready - Enter stock symbols separated by commas")
        main_layout.addWidget(self.status_label)

    def load_data(self):
        
        symbol_text = self.stock_input.text().strip()
        
        if not symbol_text:
            symbols = self.finance_machine.symbols  
        else:
           
            symbols = [s.strip().upper() for s in symbol_text.split(',')]
        
        self.status_label.setText(f"Loading data for {', '.join(symbols)}...")
        
        
        data = self.finance_machine.get_last_n_data_points(
            symbols=symbols, 
            interval="1m", 
            n_points=15
        )
        
        
        self.display_data(data)
        
        self.data_visualization.setText("Hello World!")
        
        self.status_label.setText(f"Data loaded for {', '.join(symbols)}")

    def display_data(self, data):
       
        display_text = ""
        
        for symbol, stock_data in data.items():
            display_text += f"=== {symbol} ===\n"
            
            if stock_data.empty:
                display_text += "No data available\n\n"
                continue
            
            
            display_text += stock_data[[ 'High', 'Low', 'Close']].to_string()
            display_text += "\n\n"
            
           
            latest = stock_data.iloc[-1]
            display_text += f"Latest Close: ${latest['Close']:.2f}\n"
          
            display_text += f"Data Points: {len(stock_data)}\n\n"
        
        self.data_display.setText(display_text)
        
       
        self.update_analysis(data)

    def update_analysis(self, data):
       
        analysis_text = "=== BASIC ANALYSIS ===\n\n"
        
        for symbol, stock_data in data.items():
            if stock_data.empty:
                continue
                
            latest = stock_data.iloc[-1]
            first = stock_data.iloc[0]
            
            price_change = latest['Close']-first['Close']
            percent_change = (price_change/first['Close'])*100
            
            analysis_text+= f"{symbol}:\n"
            analysis_text+=f"  First: ${first['Close']:.2f}\n"
            analysis_text+= f"  Last: ${latest['Close']:.2f}\n"
            analysis_text+=f"  Change: ${price_change:.2f} ({percent_change:+.2f}%)\n"
            analysis_text+= f"  High: ${stock_data['High'].max():.2f}\n"
            analysis_text += f"  Low: ${stock_data['Low'].min():.2f}\n\n"
        
        self.analysis_panel.setText(analysis_text)

        

    

def main():
    app = QApplication(sys.argv)
    window= MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__=="__main__":
    main()