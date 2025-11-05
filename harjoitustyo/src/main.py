

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QPushButton, QLabel,
                            QTextEdit, QSplitter)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Financial data analysis application, Leo")
        self.setGeometry(100,100,800,600)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        stock_layout = QHBoxLayout(central_widget)

        stock_layout.addWidget(QLabel("Stock symbol"))
        self.stock_input = QLineEdit()
        self.stock_input.setPlaceholderText("eg., AAPL, TSLA, GOOGL")
        self.stock_input.setFixedWidth(120)

        stock_layout.addWidget(self.stock_input)

        self.load_btn = QPushButton("Load Data")
        self.load_btn.setFixedWidth(100)
        stock_layout.addWidget(self.load_btn)

        main_layout.addLayout(stock_layout)

        content_splitter = QSplitter(Qt.Orientation.Horizontal)

        self.chart_display = QTextEdit()

        self.chart_display.setPlaceholderText("Stock chart will appears here")

        self.analysis_panel = QTextEdit()
        self.analysis_panel.setPlaceholderText("Technical analysis will appear here")

        content_splitter.addWidget(self.chart_display)
        content_splitter.addWidget(self.analysis_panel)

        content_splitter.setSizes([800,400])

        main_layout.addWidget(content_splitter)

        self.status_label = QLabel("Kokeilua, mikä ihme on status labeli")

        main_layout.addWidget(self.status_label)

    

def main():
    app = QApplication(sys.argv)
    window= MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__=="__main__":
    main()